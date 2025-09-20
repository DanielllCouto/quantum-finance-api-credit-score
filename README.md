# Quantum Finance – API de Predição de Score de Crédito

## Sobre o Projeto

Este repositório contém a **API REST de inferência** para o modelo de Machine Learning de previsão de score de crédito do projeto Quantum Finance. Desenvolvida com uma arquitetura **serverless na AWS**, esta API é a espinha dorsal para disponibilizar o modelo treinado em ambiente de produção, garantindo **escalabilidade, observabilidade e rastreabilidade**.

Integrada a um ecossistema MLOps robusto, a API consome modelos versionados via **MLflow/DagsHub** e serve previsões para aplicações downstream, como o frontend em Streamlit. Nosso foco é entregar um serviço de alta performance, seguro e com governança de modelo de ponta a ponta.

## Tecnologias e Linguagens Utilizadas

*   **Python 3.10+**: Linguagem principal para o desenvolvimento da API e lógica de inferência.
*   **AWS Lambda**: Serviço de computação serverless para execução do código da API, garantindo escalabilidade e alta disponibilidade.
*   **Amazon API Gateway**: Ponto de entrada para a API, gerenciando requisições, autenticação (API Keys) e controle de uso (Usage Plans).
*   **Amazon ECR (Elastic Container Registry)**: Repositório de imagens Docker para a containerização da função Lambda, assegurando ambientes de execução consistentes.
*   **Amazon S3 (Simple Storage Service)**: Utilizado para persistir dados de inferência em tempo real, crucial para auditoria e detecção de drift.
*   **Amazon CloudWatch**: Monitoramento abrangente com métricas personalizadas (desempenho da API, distribuição de previsões e features) e logs estruturados.
*   **MLflow/DagsHub**: Plataforma MLOps para versionamento de modelos e artefatos, permitindo que a API baixe e utilize a versão mais recente do modelo de forma rastreável.
*   **Docker**: Containerização da aplicação para portabilidade e consistência entre ambientes.
*   **GitHub Actions**: Esteira de CI/CD para automação do build, teste e deploy da API na AWS, com autenticação segura via OIDC.
*   **Pytest**: Framework para testes unitários e de integração, garantindo a qualidade do código e a funcionalidade da API.

## Competências Técnicas Demonstradas

*   **MLOps em Produção**: Implementação de um pipeline completo de MLOps, desde o versionamento de modelos até o monitoramento em produção, com foco em governança e rastreabilidade.
*   **Arquitetura Serverless na AWS**: Design e deploy de soluções escaláveis e resilientes utilizando Lambda, API Gateway, ECR, S3 e CloudWatch.
*   **Desenvolvimento de APIs Robustas**: Criação de APIs RESTful seguras, eficientes e bem documentadas, com tratamento de payload, pré-processamento de dados e integração de modelos de ML.
*   **CI/CD Avançado**: Automação de deploy com GitHub Actions e autenticação segura via OIDC, garantindo entregas contínuas e confiáveis.
*   **Qualidade de Código e Testes**: Aplicação de boas práticas de desenvolvimento, incluindo testes unitários e de integração, e análise de qualidade de código (Pylint).
*   **Gerenciamento de Modelos**: Estratégias para download dinâmico e versionamento de modelos em tempo de execução, garantindo que a API sempre utilize a versão correta e mais recente.

## Arquitetura da Solução

A arquitetura da API é baseada em princípios serverless e de MLOps, utilizando serviços da AWS para garantir escalabilidade, resiliência e observabilidade. O diagrama abaixo ilustra a interação entre os principais componentes:

<img width="1412" height="1240" alt="Arquitetura drawio" src="https://github.com/user-attachments/assets/5daf5875-b47c-4eab-ae73-5281b8363a5d" />


*Figura 1: Diagrama de Arquitetura da API de Previsão de Score de Crédito.*

## Getting Started / Guia Rápido

Quer ver a API em ação? Acesse nosso [aplicativo Streamlit de demonstração](https://quantum-finance-app-credit-score.streamlit.app/) para uma experiência interativa.

Para testar a API diretamente via cURL, solicite o endpoint e a API Key por mensagem.

### Usando cURL

```bash
curl -X POST \
  'YOUR_DEMO_API_ENDPOINT' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: YOUR_DEMO_API_KEY' \
  -d '{
    "data": {
        "idade": 30,
        "renda_anual": 75000.0,
        "salario_liquido_mensal": 4800.0,
        "qtd_contas_bancarias": 2,
        "qtd_cartoes_credito": 1,
        "taxa_juros": 3.0,
        "qtd_emprestimos": 0,
        "dias_atraso_pagamento": 0,
        "qtd_pagamentos_atrasados": 0,
        "variacao_limite_credito": 200.0,
        "qtd_consultas_credito": 1,
        "divida_pendente": 500.0,
        "percentual_utilizacao_credito": 20.0,
        "total_emprestimos_mensal": 0.0,
        "valor_investido_mensal": 1000.0,
        "saldo_mensal": 2500.0,
        "tempo_historico_credito_meses": 60,
        "ocupacao": "Developer",
        "pagamento_valor_minimo": "No",
        "comportamento_pagamento": "High_spent_Large_value_payments",
        "tipos_emprestimos": "Auto Loan"
    }
}'
```

## Tabela de Interpretação de Resultados

A API retorna um valor numérico (`prediction`) que representa a categoria de risco de crédito. A tabela abaixo detalha a interpretação de cada valor:

| Prediction | Categoria | Significado |
| :--------- | :-------- | :---------- |
| `0`        | Poor      | Alto risco de inadimplência. |
| `1`        | Standard  | Risco moderado de inadimplência. |
| `2`        | Good      | Bom perfil de crédito, baixo risco de inadimplência. |


## Checklist de Boas Práticas

Um resumo das boas práticas de MLOps e desenvolvimento aplicadas:

*   ✅ **Versionamento de Modelos (MLflow/DagsHub)**
*   ✅ **Observabilidade (CloudWatch)**
*   ✅ **Auditoria de Dados (S3)**
*   ✅ **Testes (pytest)**
*   ✅ **Segurança (API Key + Usage Plan)**
*   ✅ **CI/CD (GitHub Actions + OIDC)**
*   ✅ **Containerização (Docker/ECR)**
*   ✅ **Arquitetura Serverless (AWS Lambda)**
*   ✅ **Isolamento de Código**
*   ✅ **Payload Consistente**


## Documentação Completa

Para detalhes técnicos aprofundados sobre a arquitetura, implementação, CI/CD e muito mais, consulte a [documentação completa da API](https://github.com/DanielllCouto/quantum-finance-api-credit-score/blob/main/documentacao/documenta%C3%A7%C3%A3o_api_credit_score_quantum_finance.docx).

## Conecte-se

👨‍💻 **Daniel Estrella Couto**
[LinkedIn](https://www.linkedin.com/in/daniel-estrella-couto) | [GitHub](https://github.com/estrellacouto05)
