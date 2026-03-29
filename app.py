from src.comorbidade import comorbidades_obitos
from src.distribuicaoClassificacao import distribuicao_classificacao
from src.distribuicaoSexo import distribuicao_sexo
from src.evolucaoTemporal import evolucao_temporal
from src.faixaEtaria import faixa_etaria
from src.letalidade import taxa_letalidade
from src.sintomas import sintomas_frequentes
from src.tabelaCruzada import tabela_cruzada
from src.topMunicipios import top_municipios
from src.calcularNulos import calcular_nulos

import streamlit as st
from pyspark.sql import SparkSession
import plotly.express as px
import os

# -------------------------
# APP
# -------------------------
st.title("📊 Dashboard COVID")

# -------------------------
# Spark
# -------------------------
spark = SparkSession.builder.appName("MICRODADOS").getOrCreate()

caminho = os.path.abspath("data/MICRODADOS.csv")

df = spark.read.csv(
    caminho,
    header=True,
    sep=";",
    encoding="iso-8859-1"
)

# -------------------------
# NULOS
# -------------------------
st.subheader("Quantidade de Nulos por Coluna")

nulos_pd = calcular_nulos(df)
st.dataframe(nulos_pd)

fig = px.bar(nulos_pd, x="Coluna", y="Quantidade")
st.plotly_chart(fig, use_container_width=True)

# -------------------------
# CLASSIFICAÇÃO
# -------------------------
st.subheader("Distribuição por Classificação")

df_classificacao = distribuicao_classificacao(df)
st.dataframe(df_classificacao)

fig = px.bar(
    df_classificacao,
    x="Classificacao",
    y="Frequência Absoluta"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# TOP MUNICÍPIOS
# -------------------------
st.subheader("Top 10 Municípios")

df_top = top_municipios(df)
st.dataframe(df_top)

fig = px.bar(
    df_top,
    x="Municipio",
    y="Número de Notificações"
)

st.plotly_chart(fig, use_container_width=True)

lider = df_top.iloc[0]

st.markdown(f"""
### 🥇 Município líder  
**{lider['Municipio']}** possui **{lider['Número de Notificações']:,} notificações**
""")

# -------------------------
# SEXO
# -------------------------
st.subheader("Distribuição por Sexo")

sexo = distribuicao_sexo(df)
st.dataframe(sexo)

fig = px.pie(
    sexo,
    names="Sexo",
    values="Frequência"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# FAIXA ETÁRIA
# -------------------------
st.subheader("Faixa Etária")

faixa = faixa_etaria(df)
st.dataframe(faixa)

fig = px.bar(
    faixa,
    x="FaixaEtaria",
    y="Quantidade"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# LETALIDADE
# -------------------------
st.subheader("Taxa de Letalidade")

letal = taxa_letalidade(df)

st.write(letal)

st.markdown(f"""
Taxa de letalidade: **{letal['taxa']:.2f}%**
""")

# -------------------------
# SINTOMAS
# -------------------------
st.subheader("Sintomas mais Frequentes")

sintomas = sintomas_frequentes(df)
st.dataframe(sintomas)

fig = px.bar(
    sintomas,
    x="Sintoma",
    y="Quantidade"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# COMORBIDADES
# -------------------------
st.subheader("Comorbidades nos Óbitos")

comorb = comorbidades_obitos(df)
st.dataframe(comorb)

fig = px.bar(
    comorb,
    x="Comorbidade",
    y="Quantidade"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# TEMPORAL
# -------------------------
st.subheader("Evolução Temporal")

tempo = evolucao_temporal(df)
st.dataframe(tempo)

fig = px.line(
    tempo,
    x="AnoMes",
    y="Quantidade"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# CROSSTAB
# -------------------------
st.subheader("Tabela Cruzada")

crosstab, letalidade = tabela_cruzada(df)

st.dataframe(crosstab)

st.write("Taxa de letalidade por município:")
st.write(letalidade)