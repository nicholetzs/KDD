from pyspark.sql.functions import col, count, when, to_date, date_format
import pandas as pd

def evolucao_temporal(df):
    df = df.withColumn("DataNotificacao", to_date(col("DataNotificacao")))
    df = df.withColumn("AnoMes", date_format(col("DataNotificacao"), "yyyy-MM"))

    resultado = df.groupBy("AnoMes").count().orderBy("AnoMes")

    pdf = resultado.toPandas()
    pdf = pdf.rename(columns={"count": "Quantidade"})

    return pdf