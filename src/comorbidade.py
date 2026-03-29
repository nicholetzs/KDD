
from pyspark.sql.functions import col
import pandas as pd

def comorbidades_obitos(df):
    comorbidades = [
        'ComorbidadePulmao', 'ComorbidadeCardio', 'ComorbidadeRenal',
        'ComorbidadeDiabetes', 'ComorbidadeTabagismo', 'ComorbidadeObesidade'
    ]

    obitos = df.filter(col("Evolucao") == "Óbito pelo COVID-19")

    resultado = {}

    for c in comorbidades:
        resultado[c] = obitos.filter(col(c) == "Sim").count()

    pdf = pd.DataFrame(list(resultado.items()), columns=["Comorbidade", "Quantidade"])
    pdf = pdf.sort_values("Quantidade", ascending=False)

    return pdf
