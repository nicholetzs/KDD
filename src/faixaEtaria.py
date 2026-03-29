def faixa_etaria(df):
    resultado = df.groupBy("FaixaEtaria").count()

    pdf = resultado.toPandas()
    pdf = pdf.sort_values("FaixaEtaria")

    pdf = pdf.rename(columns={"count": "Quantidade"})

    return pdf