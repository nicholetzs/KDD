
import os
from pyspark.sql import SparkSession
import streamlit as st

@st.cache_resource
def carregar_dados():
    spark = SparkSession.builder.appName("MICRODADOS").getOrCreate()

    caminho = os.path.abspath("data/MICRODADOS.csv")

    df = spark.read.csv(
        caminho,
        header=True,
        sep=";",
        encoding="iso-8859-1"
    )
    df = df.cache()

    return df