
import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when
import pandas as pd

def calcular_nulos(df):
    num_registros = df.count()

    nulos_expr = [
        count(when(col(c).isNull() | (col(c) == ""), c)).alias(c)
        for c in df.columns
    ]

    nulos = df.select(nulos_expr).collect()[0].asDict()

    dados = []
    for coluna, qtd in nulos.items():
        if qtd > 0:
            perc = (qtd / num_registros) * 100
            dados.append((coluna, qtd, perc))

    return pd.DataFrame(
        dados,
        columns=["Coluna", "Quantidade", "Percentual (%)"]
    )