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
    now = datetime.now()
    now_formatted = now.strftime("%Y-%m-%d %H:%M:%S")

    file_name = f"{now.strftime('%Y%m%d_%H%M%S')}_credit_score_data.csv"

    data["credit_score"] = prediction
    data["timestamp"] = now_formatted
    data["model_version"] = model_info["version"]

    s3 = boto3.client('s3')

    bucket_name = 'quantum-finance'
    s3_path = 'credit-score-real-data'

    try:
        existing_object = s3.get_object(Bucket=bucket_name, Key=f"{s3_path}/{file_name}")
        existing_data = existing_object['Body'].read().decode('utf-8').strip().split('\n')
        existing_data.append(','.join(map(str, data.values())))
        update_content = '\n'.join(existing_data)

    except s3.exceptions.NoSuchKey:
        update_content = ','.join(data.keys()) + '\n' + ','.join(map(str, data.values()))

    s3.put_object(Body=update_content, Bucket=bucket_name, Key=f"{s3_path}/{file_name}")

def input_metrics(data, prediction):
