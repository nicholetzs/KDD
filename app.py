import streamlit as st
import plotly.express as px
import pandas as pd

# Configuração da página (DEVE ser a primeira linha)
st.set_page_config(
    page_title="Painel Epidemiológico COVID-19",
    page_icon="🧬",
    layout="wide", # Usa a tela inteira, estilo dashboard profissional
    initial_sidebar_state="expanded"
)

# Importações dos seus módulos
from src.carregarDados import carregar_dados
from src.calcularNulos import calcular_nulos
from src.distribuicaoClassificacao import distribuicao_classificacao
from src.topMunicipios import top_municipios
from src.distribuicaoSexo import distribuicao_sexo
from src.faixaEtaria import faixa_etaria
from src.sintomas import sintomas_frequentes
from src.comorbidade import comorbidades_obitos
from src.evolucaoTemporal import evolucao_temporal

# =========================
# ESTILIZAÇÃO CUSTOMIZADA (CSS)
# =========================
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #111d2b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# =========================
# SIDEBAR MODERNA
# =========================
with st.sidebar:
    st.image("https://www.freeiconspng.com/uploads/virus-icon-1.png", width=80)
    st.title("Navegação")
    # Trocamos o radio por um selectbox mais limpo ou botões
    secao = st.selectbox(
        "Selecione o módulo de análise:",
        ["📌 Visão Geral", "📊 Classificação & Ranking", "👥 Perfil Demográfico", "🏥 Análise Clínica", "📅 Evolução Temporal"]
    )
    st.divider()
    st.info("Projeto KDD - Análise de Microdados")

# =========================
# CARREGAMENTO DE DADOS
# =========================
with st.spinner("Sincronizando base de dados..."):
    df = carregar_dados()

# =========================
# HEADER CIENTÍFICO
# =========================
col_tit, col_logo = st.columns([4, 1])
with col_tit:
    st.title("🧬 Monitoramento Epidemiológico — COVID-19")
    st.caption("Estudo fundamentado em Processo de KDD (Knowledge Discovery in Databases)")

# Métricas Rápidas (KPIs) no topo
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total de Notificações", f"{len(df):,}")
m2.metric("Municípios Analisados", df['Municipio'].nunique())
m3.metric("Status", "Amostra Otimizada")
m4.metric("Versão", "2026.1")

st.divider()

# =========================
# LÓGICA DAS SEÇÕES
# =========================

if secao == "📌 Visão Geral":
    st.subheader("🔍 Diagnóstico da Integridade dos Dados")
    nulos = calcular_nulos(df)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("Registros ausentes por variável:")
        st.dataframe(nulos, use_container_width=True)
    with col2:
        fig = px.bar(nulos, x="Coluna", y="Quantidade", color="Quantidade", color_continuous_scale="Reds", title="Missing Values (Nulos)")
        st.plotly_chart(fig, use_container_width=True)

elif secao == "📊 Classificação & Ranking":
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📍 Ranking de Municípios")
        dados_mun = top_municipios(df)
        fig_mun = px.bar(dados_mun, x="Número de Notificações", y="Municipio", orientation='h', color="Número de Notificações", title="Top 10 Municípios (Volume)")
        st.plotly_chart(fig_mun, use_container_width=True)
        
    with c2:
        st.subheader("📋 Classificação de Casos")
        dados_class = distribuicao_classificacao(df)
        fig_class = px.pie(dados_class, names="Classificacao", values="Frequência Absoluta", hole=0.4, title="Status das Notificações")
        st.plotly_chart(fig_class, use_container_width=True)

elif secao == "👥 Perfil Demográfico":
    st.subheader("👥 Perfil Populacional")
    col1, col2 = st.columns(2)
    
    with col1:
        sexo = distribuicao_sexo(df)
        fig_sexo = px.pie(sexo, names="Sexo", values="Frequência", title="Distribuição por Sexo", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_sexo, use_container_width=True)
        
    with col2:
        faixa = faixa_etaria(df)
        fig_faixa = px.bar(faixa, x="FaixaEtaria", y="Quantidade", title="Pirâmide Etária (Amostra)", color_discrete_sequence=['#4c78a8'])
        st.plotly_chart(fig_faixa, use_container_width=True)

elif secao == "🏥 Análise Clínica":
    st.subheader("🩺 Indicadores Clínicos e Comorbidades")
    
    tab1, tab2 = st.tabs(["Sintomas Frequentes", "Comorbidades (Óbitos)"])
    
    with tab1:
        sintomas = sintomas_frequentes(df)
        fig_sint = px.bar(sintomas, x="Quantidade", y="Sintoma", orientation='h', title="Prevalência de Sintomas", color="Quantidade")
        st.plotly_chart(fig_sint, use_container_width=True)
        
    with tab2:
        comorb = comorbidades_obitos(df)
        fig_com = px.treemap(comorb, path=['Comorbidade'], values='Quantidade', title="Mapa de Calor: Comorbidades Associadas")
        st.plotly_chart(fig_com, use_container_width=True)

elif secao == "📅 Evolução Temporal":
    st.subheader("📈 Série Temporal de Notificações")
    tempo = evolucao_temporal(df)
    fig_tempo = px.area(tempo, x="AnoMes", y="Quantidade", title="Progressão Mensal de Casos", line_shape="spline", color_discrete_sequence=['#1f77b4'])
    st.plotly_chart(fig_tempo, use_container_width=True)