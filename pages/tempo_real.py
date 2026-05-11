import streamlit as st
import pandas as pd
import os
import glob
import re
import unicodedata
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

RELATORIOS_PATH = os.getenv("RELATORIOS_PATH")

COLABORADORES = {
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

st.set_page_config(page_title="Ligações 3CX — Tempo Real", layout="wide")
st.title("Ligações 3CX — Tempo Real")

def normalizar(txt):
    txt = str(txt).lower().strip()
    txt = unicodedata.normalize("NFKD", txt)
    return "".join(c for c in txt if not unicodedata.combining(c))

def extrair_nome(texto):
    texto = str(texto).lower()
    texto = re.sub(r'\(.*?\)', '', texto)
    for setor in ["vendas diretas", "cursos de odontologia", "cursos de ortodontia",
                  "franquias e credenciados", "franquias", "myobrace",
                  "grandes clínicas", "grandes clinicas"]:
        if setor in texto:
            texto = texto.split(setor)[0]
            break
    texto = re.sub(r'\d+', '', texto)
    return texto.replace("-", " ").strip().title()

def extrair_setor(txt):
    txt = str(txt)
    if "Cursos de Ortodontia" in txt or "Cursos de Odontologia" in txt or "Camila" in txt:
        return "Cursos e Distribuição"
    if "Grandes Clínicas" in txt or "Grandes Clinicas" in txt:
        return "Grandes Clínicas"
    if "Vendas Diretas" in txt:
        return "Vendas Diretas"
    if "Franquias e Credenciados" in txt:
        return "Franquias e Credenciados"
    if "Myobrace" in txt:
        return "Myobrace"
    return None

def converter_tempo(t):
    try:
        h, m, s = map(int, str(t).split(":"))
        return h * 3600 + m * 60 + s
    except:
        return 0

def processar(caminho):
    df = pd.read_csv(caminho)
    df["Setor"] = df["From"].apply(extrair_setor)
    df = df[df["Setor"].notna()].copy()
    df["Usuario"] = df["From"].apply(extrair_nome)
    df["Usuario_norm"] = df["Usuario"].apply(normalizar)
    df["Status_Classificado"] = df["Status"].map({
        "Answered": "Atendida",
        "Unanswered": "Não Atendida"
    }).fillna("Outro")
    df["Tempo_Segundos"] = df["Talking"].apply(converter_tempo)
    return df

def gerar_tabela(df, setor):
    df_setor = df[df["Setor"] == setor]
    resumo = df_setor.groupby("Usuario_norm").agg(
        Total=("Usuario", "count"),
        Atendidas=("Status_Classificado", lambda x: (x == "Atendida").sum()),
        NAtendidas=("Status_Classificado", lambda x: (x == "Não Atendida").sum()),
        Tempo=("Tempo_Segundos", "sum")
    ).reset_index()

    base = pd.DataFrame({"Usuario": COLABORADORES[setor]})
    base["Usuario_norm"] = base["Usuario"].apply(normalizar)
    resumo = base.merge(resumo, on="Usuario_norm", how="left").fillna(0)

    resumo["% Atend"] = resumo.apply(
        lambda x: round(x["Atendidas"] / x["Total"] * 100, 1) if x["Total"] > 0 else 0, axis=1
    )
    resumo["Tempo"] = resumo["Tempo"].apply(
        lambda x: f"{int(x//3600):02d}:{int((x%3600)//60):02d}:{int(x%60):02d}"
    )
    resumo = resumo.sort_values("Total", ascending=False)
    return resumo[["Usuario", "Total", "Atendidas", "% Atend", "NAtendidas", "Tempo"]]

if not RELATORIOS_PATH or not os.path.exists(RELATORIOS_PATH):
    st.error("Caminho de relatórios não configurado ou não encontrado.")
    st.stop()

arquivos = sorted(glob.glob(os.path.join(RELATORIOS_PATH, "*.csv")), key=os.path.getmtime, reverse=True)

if not arquivos:
    st.warning("Nenhum arquivo CSV encontrado.")
    st.stop()

caminho = arquivos[0]
hora = datetime.fromtimestamp(os.path.getmtime(caminho)).strftime("%d/%m/%Y %H:%M")
st.caption(f"Arquivo: {os.path.basename(caminho)} ({hora})")

df = processar(caminho)

for setor in COLABORADORES.keys():
    st.subheader(setor)
    tabela = gerar_tabela(df, setor)
    st.dataframe(tabela, use_container_width=True, hide_index=True)