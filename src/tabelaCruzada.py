import pandas as pd
from pyspark.sql.functions import col

def tabela_cruzada(df):
    top5 = (
        df.groupBy("Municipio")
        .count()
        .orderBy("count", ascending=False)
        .limit(5)
    )

    top5_lista = [row["Municipio"] for row in top5.collect()]

    filtrado = df.filter(col("Municipio").isin(top5_lista))

    pdf = filtrado.toPandas()

    crosstab = pd.crosstab(pdf["Municipio"], pdf["Evolucao"])

    letalidade = {}

    for municipio in crosstab.index:
        total = crosstab.loc[municipio].sum()
        obitos = crosstab.loc[municipio].get("Óbito pelo COVID-19", 0)

        taxa = (obitos / total) * 100 if total > 0 else 0
        letalidade[municipio] = taxa

    return crosstab, letalidade