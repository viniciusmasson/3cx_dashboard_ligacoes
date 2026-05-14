# 3CX Dashboard — Ligações por Setor

Automação de extração e visualização de relatórios de chamadas do 3CX, sistema PABX em nuvem.

## O problema

O 3CX gera relatórios de chamadas pela interface web, mas não expõe esses dados via API no formato necessário. Acompanhar o volume de ligações por colaborador e por setor exigia acesso manual à plataforma, download de CSV e tratamento no Excel.

## A solução

Dois coletores com comportamentos distintos, dependendo do caso de uso:

- **coletor_historico.py** — aplica filtro de data (D-1) e baixa o relatório do dia anterior; ideal para consolidação diária
- **coletor_tempo_real.py** — baixa sempre o relatório mais recente sem filtro, para monitoramento contínuo durante o expediente
- **dashboard.py** — exibe ligações por colaborador agrupadas por setor, com seletor de arquivo para análise histórica
- **pages/tempo_real.py** — página dedicada que carrega automaticamente o arquivo mais recente

A separação entre coleta histórica e tempo real foi uma decisão deliberada: relatórios com filtro de data são mais lentos para gerar no 3CX, o que tornava um coletor único inadequado para atualização frequente.

## Stack

Python · Selenium · Streamlit · Pandas · python-dotenv

## Como rodar localmente

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Copie `.env.example` para `.env` e preencha com suas credenciais
4. Para gerar dados de demonstração: `python gerar_dados_mock.py`
5. Para rodar o dashboard: `streamlit run dashboard.py`
6. Para rodar o coletor histórico: `python coletor_historico.py`
7. Para rodar o coletor tempo real: `python coletor_tempo_real.py`

> O `gerar_dados_mock.py` cria dados fictícios para testar o dashboard sem acesso ao 3CX.

## Estrutura

- coletor_historico.py — Automação Selenium com filtro por data
- coletor_tempo_real.py — Automação Selenium sem filtro de data
- dashboard.py — Dashboard Streamlit com seletor de arquivo
- pages/tempo_real.py — Página de visualização em tempo real
- gerar_dados_mock.py — Gerador de dados fictícios para demo
- requirements.txt
- .env.example — Template de variáveis de ambiente
- data/ — Relatórios baixados (ignorado pelo git)

## Preview

![Dashboard](preview.png)
