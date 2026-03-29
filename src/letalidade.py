from pyspark.sql.functions import col, count, when, to_date, date_format
import pandas as pd

import streamlit as st

def taxa_letalidade(df):
    confirmados = df.filter(col("Classificacao") == "Confirmados")

    total = confirmados.count()

    obitos_covid = confirmados.filter(col("Evolucao") == "Óbito pelo COVID-19").count()
    obitos_outras = confirmados.filter(col("Evolucao") == "Óbito por outras causas").count()
    cura = confirmados.filter(col("Evolucao") == "Cura").count()
    ignorado = confirmados.filter(col("Evolucao") == "Ignorado").count()

    taxa = (obitos_covid / total) * 100 if total > 0 else 0

    return {
        "total": total,
        "obitos_covid": obitos_covid,
        "obitos_outras": obitos_outras,
        "cura": cura,
        "ignorado": ignorado,
        "taxa": taxa
    }
