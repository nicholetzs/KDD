import pandas as pd


def evolucao_temporal(df):
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

    df["AnoMes"] = df["Data"].dt.to_period("M")

    dados = df.groupby("AnoMes").size().reset_index(name="Quantidade")

    return dados