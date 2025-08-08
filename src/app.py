"""
Função para executar predição de valor de laptop com base nos parâmetros enviados, 
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

    file_name = f"data/real_data_{now.strftime('%Y%m%d_%H%M%S')}_credit_score_data.csv"

    