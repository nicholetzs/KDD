import pandas as pd

def top_municipios(df):
    resultado = (
        df.groupBy("Municipio")
        .count()
        .orderBy("count", ascending=False)
        .limit(10)
    )

    pdf = resultado.toPandas()

    pdf = pdf.rename(columns={
        "count": "Número de Notificações"
    })

    return pdf