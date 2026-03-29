
import streamlit as st
import plotly.express as px

from src.carregarDados import carregar_dados
from src.calcularNulos import calcular_nulos
from src.distribuicaoClassificacao import distribuicao_classificacao
from src.topMunicipios import top_municipios
from src.distribuicaoSexo import distribuicao_sexo
from src.faixaEtaria import faixa_etaria
from src.letalidade import taxa_letalidade
from src.sintomas import sintomas_frequentes
from src.comorbidade import comorbidades_obitos
from src.evolucaoTemporal import evolucao_temporal
from src.tabelaCruzada import tabela_cruzada

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚙️ Controles")

secao = st.sidebar.radio(
    "Escolha a análise:",
    [
        "Visão Geral",
        "Classificação",
        "Municípios",
        "Perfil Demográfico",
        "Clínico",
        "Temporal"
    ]
)

# =========================
# TÍTULO
# =========================
st.title("📊 Painel Epidemiológico — COVID-19")
st.caption("PySpark + Streamlit + Plotly")
st.divider()

# =========================
# DADOS
# =========================
with st.spinner("Carregando dados..."):
    df = carregar_dados()

# =========================
# VISÃO GERAL
# =========================
if secao == "Visão Geral":

    st.subheader("Qualidade dos Dados")

    with st.spinner("Calculando nulos..."):
        nulos = calcular_nulos(df)

    st.dataframe(nulos)

    fig = px.bar(nulos, x="Coluna", y="Quantidade")
    st.plotly_chart(fig, use_container_width=True)

# =========================
# CLASSIFICAÇÃO
# =========================
elif secao == "Classificação":

    st.subheader("Distribuição por Classificação")

    with st.spinner("Calculando classificação..."):
        dados = distribuicao_classificacao(df)

    st.dataframe(dados)

    fig = px.bar(
        dados,
        x="Classificacao",
        y="Frequência Absoluta"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# MUNICÍPIOS
# =========================
elif secao == "Municípios":

    st.subheader("Top 10 Municípios")

    with st.spinner("Calculando ranking..."):
        dados = top_municipios(df)

    st.dataframe(dados)

    fig = px.bar(
        dados,
        x="Municipio",
        y="Número de Notificações"
    )

    st.plotly_chart(fig, use_container_width=True)

    lider = dados.iloc[0]

    st.success(
        f"{lider['Municipio']} lidera com {lider['Número de Notificações']:,} casos"
    )

# =========================
# PERFIL DEMOGRÁFICO
# =========================
elif secao == "Perfil Demográfico":

    # Sexo
    st.subheader("Sexo")

    with st.spinner("Calculando sexo..."):
        sexo = distribuicao_sexo(df)

    st.dataframe(sexo)

    fig = px.pie(
        sexo,
        names="Sexo",
        values="Frequência"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Faixa etária
    st.subheader("Faixa Etária")

    with st.spinner("Calculando faixa etária..."):
        faixa = faixa_etaria(df)

    st.dataframe(faixa)

    fig = px.bar(
        faixa,
        x="FaixaEtaria",
        y="Quantidade"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# CLÍNICO
# =========================
elif secao == "Clínico":

    # Letalidade
    st.subheader("Taxa de Letalidade")

    with st.spinner("Calculando letalidade..."):
        letal = taxa_letalidade(df)

    st.metric("Taxa (%)", f"{letal['taxa']:.2f}")

    # Sintomas
    st.subheader("Sintomas")

    with st.spinner("Calculando sintomas..."):
        sintomas = sintomas_frequentes(df)

    st.dataframe(sintomas)

    fig = px.bar(
        sintomas,
        x="Sintoma",
        y="Quantidade"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Comorbidades
    st.subheader("Comorbidades")

    with st.spinner("Calculando comorbidades..."):
        comorb = comorbidades_obitos(df)

    st.dataframe(comorb)

    fig = px.bar(
        comorb,
        x="Comorbidade",
        y="Quantidade"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TEMPORAL
# =========================
elif secao == "Temporal":

    st.subheader("Evolução Temporal")

    with st.spinner("Calculando série temporal..."):
        tempo = evolucao_temporal(df)

    st.dataframe(tempo)

    fig = px.line(
        tempo,
        x="AnoMes",
        y="Quantidade"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Crosstab
    st.subheader("Tabela Cruzada")

    with st.spinner("Calculando cruzamento..."):
        crosstab, letalidade = tabela_cruzada(df)

    st.dataframe(crosstab)

    st.write("Letalidade por município:")
    st.write(letalidade)