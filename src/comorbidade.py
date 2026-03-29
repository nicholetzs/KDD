import pandas as pd


def comorbidades_obitos(df):
    df_obitos = df[df["Evolucao"] == "Óbito pelo COVID-19"]

    cols = ["Diabetes", "Cardiopatia", "Obesidade"]

    dados = {}
    for col in cols:
        dados[col] = (df_obitos[col] == "Sim").sum()

    return (
        pd.DataFrame(list(dados.items()), columns=["Comorbidade", "Quantidade"])
        .sort_values(by="Quantidade", ascending=False)
    )