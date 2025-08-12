"""
Função para executar predição do score de crédito com base nos parâmetros enviados, 
como modelo, processador, memória etc.
Utiliza modelo que precisa ser baixado do repositório de registro de modelos em toda 
implantação nova.
"""

from datetime import datetime
import json
import boto3
import joblib

model = joblib.load('model/model.pkl')

with open('model/model_metadata.json', 'r', encoding="utf-8") as f:
    model_info = json.load(f)

cloudwatch = boto3.client('cloudwatch')

def write_real_data(data, prediction):
    """
    Função para escrever os dados consumidos para depois serem estudados 
    para desvios de dados, modelo ou conceito.

    Args:
        data (dict): dicionário de dados com todos os atributos.
        prediction (int): valor de predição.
    """
    # Marca temporal para auditoria
    now = datetime.now()
    now_formatted = now.strftime("%Y-%m-%d %H:%M:%S")

    # Nome do arquivo inclui timestamp no formato YYYYMMDD_HHMMSS 
    # para evitar colisão e manter histórico de inferências
    file_name = f"{now.strftime('%Y%m%d_%H%M%S')}_credit_score_data.csv"

    data["credit_score"] = prediction
    data["timestamp"] = now_formatted
    data["model_version"] = model_info["version"]

    s3 = boto3.client('s3')

    bucket_name = 'quantum-finance'
    s3_path = 'credit-score-real-data'

    try:
        # Se o arquivo já existir, adiciona novo registro ao final
        existing_object = s3.get_object(Bucket=bucket_name, Key=f"{s3_path}/{file_name}")
        existing_data = existing_object['Body'].read().decode('utf-8').strip().split('\n')
        existing_data.append(','.join(map(str, data.values())))
        update_content = '\n'.join(existing_data)

    except s3.exceptions.NoSuchKey:
        # Primeiro registro para este timestamp → cria cabeçalho + registro inicial
        update_content = ','.join(data.keys()) + '\n' + ','.join(map(str, data.values()))

    # Upload no S3 — cada arquivo é identificado por timestamp único
    s3.put_object(Body=update_content, Bucket=bucket_name, Key=f"{s3_path}/{file_name}")

def input_metrics(data, prediction):
    """
    Função para escrever métricas customizadas no Cloudwatch.

    Args:
        data (dict): dicionário de dados com todos os atributos.
        prediction (int): valor de predição.
    """
    # Mapeamento de classes numéricas para rótulos de risco
    RISK_CATEGORY_MAP = {
        0: "Poor",
        1: "Standard",
        2: "Good"
    }

    # Obtém o rótulo da predição
    prediction_label = RISK_CATEGORY_MAP.get(prediction, "Unknown")

    # Envia métrica de predição para o CloudWatch
    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'Credit Score Prediction',
                'Value': prediction,
                'Dimensions': [{'Name': "RiskCategory", 'Value': prediction_label}]
            },
        ], Namespace='Credit Score Model'
    )

    # Registra no CloudWatch cada feature recebida na requisição como uma métrica independente.
    for key, value in data.items():
        cloudwatch.put_metric_data(
            MetricData=[
                {
                    'MetricName': 'Client Feature',  
                    'Value': 1,                      
                    'Unit': 'Count',
                    'Dimensions': [
                        {'Name': key, 'Value': str(value)}  
                    ]
                },
            ],
            Namespace='Credit Score Features'
        )
def prepare_payload(data):
    """
    Função para padronizar o payload de entrada de modo
    a ser compatível com a execução do modelo.

    Args:
        data (dict): dicionário de dados com todos os atributos.

     Returns:
        dict: payload padronizado.

    """
    data_processed = []

    # Conversões para float ou int conforme o tipo original no dataset
    data_processed.append(float(data["idade"]))
    data_processed.append(float(data["renda_anual"]))
    data_processed.append(float(data["salario_liquido_mensal"]))
    data_processed.append(float(data["qtd_contas_bancarias"]))
    data_processed.append(int(data["qtd_cartoes_credito"]))
    data_processed.append(float(data["taxa_juros"]))
    data_processed.append(float(data["qtd_emprestimos"]))
    data_processed.append(int(data["dias_atraso_pagamento"]))
    data_processed.append(float(data["qtd_pagamentos_atrasados"]))
    data_processed.append(float(data["variacao_limite_credito"]))
    data_processed.append(float(data["qtd_consultas_credito"]))
    data_processed.append(float(data["divida_pendente"]))
    data_processed.append(float(data["percentual_utilizacao_credito"]))
    data_processed.append(float(data["total_emprestimos_mensal"]))
    data_processed.append(float(data["valor_investido_mensal"]))
    data_processed.append(float(data["saldo_mensal"]))
    data_processed.append(int(data["tempo_historico_credito_meses"]))

    # Dicionário de categorias, excluindo as referências dropadas
    conditions = {
        # ocupacao – Opção Accountant se nenhuma condição satisfazer
        "ocupacao": {
            "Architect", "Developer", "Doctor", "Engineer", "Entrepreneur",
            "Journalist", "Lawyer", "Manager", "Mechanic", "Media_Manager",
            "Musician", "Not Informed", "Scientist", "Teacher", "Writer"
        },

        # pagamento_valor_minimo – Opção No se nenhuma condição satisfazer
        "pagamento_valor_minimo": {
            "Not Informed", "Yes"
        },

        # comportamento_pagamento – Opção High_spent_Large_value_payments se nenhuma condição satisfazer
        "comportamento_pagamento": {
            "High_spent_Medium_value_payments", "High_spent_Small_value_payments",
            "Low_spent_Large_value_payments", "Low_spent_Medium_value_payments",
            "Low_spent_Small_value_payments"
        },

        # tipos_emprestimos – Opção Auto Loan se nenhuma condição satisfazer
        "tipos_emprestimos": {
            "Credit-Builder Loan", "Debt Consolidation Loan", "Home Equity Loan",
            "Mortgage Loan", "Not Specified", "Payday Loan", "Personal Loan",
            "Student Loan", "Two or More Types of Loan"
        }
    }

    # Loop para gerar o vetor de dummies na ordem definida
    for key, values in conditions.items():
        for value in values:
            data_processed.append(True if data[key] == value else False)

    return data_processed
def handler(event, context=False):
    """
    Função principal de execução da API no AWS Lambda.

    - Recebe evento vindo do API Gateway (ou execução direta no Lambda)
    - Extrai dados enviados no payload
    - Processa dados brutos no formato esperado pelo modelo
    - Executa predição e retorna o resultado
    - Registra métricas no CloudWatch e salva dados reais no S3

    Args:
        event (json): Payload para processamento (API Gateway ou chamada direta).
        context (json): Metadados de execução no Lambda (opcional).

    Returns:
        dict: Resposta no formato esperado pelo API Gateway.
    """

    # Logs de depuração (úteis para CloudWatch)
    print(event)
    print(context)

    # Se a chamada vier do API Gateway, o payload estará em event["body"] como string JSON
    if "body" in event:
        print("Body found in event, invoked by API Gateway")

        body_str = event.get("body", "{}")
        body = json.loads(body_str)  # Converte string JSON para dict
        print(body)

        data = body.get("data", {})  # Extrai chave 'data' do body

    else:
        # Execução direta do Lambda (sem API Gateway)
        print("Body not found in event, invoked by Lambda")

        data = event.get("data", {})  # Extrai chave 'data' diretamente do evento

    print(data)

    # Prepara dados de entrada no formato esperado pelo modelo
    data_processed = prepare_payload(data)

    # Executa predição
    prediction = model.predict([data_processed])
    prediction = int(prediction[0])  # Converte para int simples para serialização JSON

    print(f"Prediction: {prediction}")

    # Registra métricas no CloudWatch (monitoramento de desempenho e comportamento)
    input_metrics(data, prediction)

    # Salva dados reais e predição no S3 (auditoria e detecção de drift)
    write_real_data(data, prediction)

    # Retorna resposta HTTP no formato esperado pelo API Gateway
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "prediction": prediction,
            "version": model_info["version"],  # Versão do modelo em uso
        })
    }
# Fim do arquivo src/app.py
# Este é o ponto de entrada para a execução do Lambda ou API Gateway