from pyspark.sql.functions import col, count
import pandas as pd

def tabela_cruzada(df):

    # -------------------------
    # TOP 5 MUNICÍPIOS
    # -------------------------
    top5 = (
        df.groupBy("Municipio")
        .count()
        .orderBy("count", ascending=False)
        .limit(5)
    )

    top5_lista = [row["Municipio"] for row in top5.collect()]

    # -------------------------
    # FILTRAR
    # -------------------------
    filtrado = df.filter(col("Municipio").isin(top5_lista))

    # -------------------------
    # 🔥 AGRUPAMENTO NO SPARK
    # -------------------------
    agrupado = (
        filtrado
        .groupBy("Municipio", "Evolucao")
        .count()
    )

    # -------------------------
    # 🔥 AGORA SIM (pequeno!)
    # -------------------------
    pdf = agrupado.toPandas()

    # -------------------------
    # PIVOT
    # -------------------------
    crosstab = pdf.pivot(
        index="Municipio",
        columns="Evolucao",
        values="count"
    ).fillna(0)

    # -------------------------
    # LETALIDADE
    # -------------------------
    letalidade = {}

    for municipio in crosstab.index:
        total = crosstab.loc[municipio].sum()
        obitos = crosstab.loc[municipio].get("Óbito pelo COVID-19", 0)

        taxa = (obitos / total) * 100 if total > 0 else 0
        letalidade[municipio] = taxa

    return crosstab, letalidade