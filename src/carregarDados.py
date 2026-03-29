import pandas as pd
import streamlit as st
import os

@st.cache_data
def carregar_dados():
    caminho = os.path.abspath("data/MICRODADOS_DIVERSIFICADO.csv")

    df = pd.read_csv(
        caminho,
        sep=";",
        encoding="iso-8859-1",
        low_memory=False

    )

    # OTIMIZAÇÃO CRÍTICA
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("category")

    return df