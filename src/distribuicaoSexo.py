
from pyspark.sql.functions import col
import pandas as pd
import streamlit as st

def distribuicao_sexo(df):
    total = df.count()

    resultado = df.groupBy("Sexo").count()

    resultado = resultado.withColumn(
        "Percentual (%)",
        (col("count") / total) * 100
    )

    pdf = resultado.toPandas()
    pdf = pdf.rename(columns={"count": "Frequência"})

    return pdf