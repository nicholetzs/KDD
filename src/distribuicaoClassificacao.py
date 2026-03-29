
from pyspark.sql.functions import col
import pandas as pd
import streamlit as st

def distribuicao_classificacao(df):
    total = df.count()

    resultado = df.groupBy("Classificacao").count()

    resultado = resultado.withColumn(
        "Percentual (%)",
        (col("count") / total) * 100
    )

    pdf = resultado.toPandas()

    pdf = pdf.rename(columns={
        "count": "Frequência Absoluta"
    })

    return pdf.sort_values("Frequência Absoluta", ascending=False)