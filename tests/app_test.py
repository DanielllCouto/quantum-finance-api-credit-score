# tests/test_app.py
from pathlib import Path
import json
import types
import src.app as app

def test_model_exists():
    assert Path("model/model.pkl").is_file(), "Model file does not exist at model/model.pkl"

def test_model_version_exists():
    assert Path("model/model_metadata.json").is_file(), "Model version file does not exist at model/model_metadata.json"

def test_handler_call_local_without_aws(monkeypatch):
    # 1) Neutraliza CloudWatch e S3
    monkeypatch.setattr(app, "input_metrics", lambda data, pred: None)
    monkeypatch.setattr(app, "write_real_data", lambda data, pred: None)

    # 2) Payload de teste
    payload = {
        "idade": 35,
        "renda_anual": 85000.0,
        "salario_liquido_mensal": 5500.0,
        "qtd_contas_bancarias": 3,
        "qtd_cartoes_credito": 2,
        "taxa_juros": 2.5,
        "qtd_emprestimos": 1,
        "dias_atraso_pagamento": 0,
        "qtd_pagamentos_atrasados": 0,
        "variacao_limite_credito": 500.0,
        "qtd_consultas_credito": 2,
        "divida_pendente": 1500.0,
        "percentual_utilizacao_credito": 35.5,
        "total_emprestimos_mensal": 800.0,
        "valor_investido_mensal": 1200.0,
        "saldo_mensal": 3000.0,
        "tempo_historico_credito_meses": 72,
        "ocupacao": "Engineer",
        "pagamento_valor_minimo": "Yes",
        "comportamento_pagamento": "Low_spent_Medium_value_payments",
        "tipos_emprestimos": "Personal Loan"
    }

    # 3) Execução direta (sem API Gateway)
    event = {"data": payload}
    resp = app.handler(event, None)
    body = json.loads(resp["body"])

    assert resp["statusCode"] == 200
    assert isinstance(body["prediction"], int)
    assert body["prediction"] >= 0
    assert "version" in body and isinstance(body["version"], str)

def test_handler_call_via_apigw_body(monkeypatch):
    # Neutraliza AWS
    monkeypatch.setattr(app, "input_metrics", lambda data, pred: None)
    monkeypatch.setattr(app, "write_real_data", lambda data, pred: None)

    payload = {
        "data": {
            "idade": 35,
            "renda_anual": 85000.0,
            "salario_liquido_mensal": 5500.0,
            "qtd_contas_bancarias": 3,
            "qtd_cartoes_credito": 2,
            "taxa_juros": 2.5,
            "qtd_emprestimos": 1,
            "dias_atraso_pagamento": 0,
            "qtd_pagamentos_atrasados": 0,
            "variacao_limite_credito": 500.0,
            "qtd_consultas_credito": 2,
            "divida_pendente": 1500.0,
            "percentual_utilizacao_credito": 35.5,
            "total_emprestimos_mensal": 800.0,
            "valor_investido_mensal": 1200.0,
            "saldo_mensal": 3000.0,
            "tempo_historico_credito_meses": 72,
            "ocupacao": "Engineer",
            "pagamento_valor_minimo": "Yes",
            "comportamento_pagamento": "Low_spent_Medium_value_payments",
            "tipos_emprestimos": "Personal Loan"
        }
    }

    # Simula evento do API Gateway (body string)
    event = {"body": json.dumps(payload)}
    resp = app.handler(event, None)
    body = json.loads(resp["body"])

    assert resp["statusCode"] == 200
    assert isinstance(body["prediction"], int)
    assert "version" in body
