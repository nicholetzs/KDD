import pandas as pd


def sintomas_frequentes(df):
    sintomas_cols = ["Febre", "Tosse", "Garganta", "Dispneia"]

    dados = {}
    for col in sintomas_cols:
        dados[col] = (df[col] == "Sim").sum()

    return (
        pd.DataFrame(list(dados.items()), columns=["Sintoma", "Quantidade"])
        .sort_values(by="Quantidade", ascending=False)
    )