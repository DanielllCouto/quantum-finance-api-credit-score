"""
Este script realiza o download da versão mais recente de um modelo registrado no MLflow Tracking Server
(hospedado no Dagshub) e salva os metadados associados localmente.
"""
from mlflow.tracking import MlflowClient
import mlflow
import json
from datetime import datetime

print("Downloading the latest model version...")

# Define a URI de rastreamento do MLflow (Dagshub)
mlflow.set_tracking_uri("https://dagshub.com/estrellacouto05/quantum-finance-credit-score.mlflow")

model_name = "credit-score-model"
artifact_relative_path = "model/model.pkl"

client = MlflowClient()

# Busca por todas as versões registradas do modelo 
# Identifica a versão mais recente com base no número da versão
versions = client.search_model_versions(f"name='{model_name}'")
latest_version = max(versions, key=lambda v: int(v.version))

download_path = client.download_artifacts(
    run_id=latest_version.run_id,
    path=artifact_relative_path,
    dst_path="."
)

print(f"Latest model version: {latest_version.version}")
print(f"Model run ID: {latest_version.run_id}")

print(f"Writing model metadata...")

# Criação do arquivo de metadados do modelo
model_metadata = {
    "model_name": model_name,
    "version": latest_version.version,
    "run_id": latest_version.run_id,
    "source": latest_version.source,
    "downloaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Salvando os metadados em um arquivo JSON
with open("model/model_metadata.json", "w") as f:
    json.dump(model_metadata, f, indent=2)

print(f"Latest model downloaded successfully in path {download_path}")