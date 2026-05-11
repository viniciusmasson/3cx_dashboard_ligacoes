from faker import Faker
import pandas as pd
import os
import random

fake = Faker("pt_BR")
Faker.seed(42)
random.seed(42)

colaboradores = {
    "Vendas Diretas": [
        "Adriano Fonseca", "Beatriz Cavalcanti", "César Drummond",
        "Débora Nunes", "Fábio Queiroz", "Helena Borba",
        "Iago Monteiro", "Juliana Prado", "Kleber Tavares",
    ],
    "Cursos e Distribuição": [
        "Laura Menezes", "Márcio Esteves", "Natália Cunha",
    ],
    "Franquias e Credenciados": [
        "Otávio Braga", "Priscila Lemos", "Rafael Cardoso",
        "Sabrina Moura", "Thiago Vieira", "Ursula Campos",
        "Vanda Freitas", "Wilson Paz",
    ],
    "Myobrace": [
        "Xavier Ramos", "Yara Pinheiro", "Zilda Correia",
        "André Lacerda", "Bruna Guimarães", "Cláudio Mesquita",
        "Diana Rocha", "Emerson Teles",
    ],
    "Grandes Clínicas": [
        "Flávia Andrade", "Gustavo Peixoto", "Iara Sampaio",
        "Jonas Carvalho", "Karen Magalhães", "Leandro Souza",
        "Mônica Ferraz", "Nuno Batista",
    ],
}

setor_para_coluna = {
    "Vendas Diretas": "Vendas Diretas",
    "Cursos e Distribuição": "Cursos de Ortodontia",
    "Franquias e Credenciados": "Franquias e Credenciados",
    "Myobrace": "Myobrace",
    "Grandes Clínicas": "Grandes Clínicas",
}

os.makedirs("data", exist_ok=True)

datas = ["2025-05-01", "2025-05-02", "2025-05-05"]

for data in datas:
    linhas = []
    for setor, agentes in colaboradores.items():
        setor_coluna = setor_para_coluna[setor]
        for agente in agentes:
            for _ in range(random.randint(3, 15)):
                segundos = random.randint(0, 3600)
                h = segundos // 3600
                m = (segundos % 3600) // 60
                s = segundos % 60
                linhas.append({
                    "From": f"{agente} - {setor_coluna} ({random.randint(1000,9999)})",
                    "Status": random.choice(["Answered", "Answered", "Unanswered"]),
                    "Talking": f"{h:02d}:{m:02d}:{s:02d}",
                })
    pd.DataFrame(linhas).to_csv(f"data/relatorio_chamadas_{data}.csv", index=False)

print("Dados mock gerados em /data")