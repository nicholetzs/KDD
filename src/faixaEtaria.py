import pandas as pd

def faixa_etaria(df):
    bins = [0, 18, 30, 45, 60, 75, 100]
    labels = ["0-18", "19-30", "31-45", "46-60", "61-75", "76+"]

    df["FaixaEtaria"] = pd.cut(df["IdadeNaDataNotificacao"], bins=bins, labels=labels)

    dados = df["FaixaEtaria"].value_counts().sort_index().reset_index()
    dados.columns = ["FaixaEtaria", "Quantidade"]

    return dados