import pandas as pd
from pyspark.sql.functions import col

def sintomas_frequentes(df):
    sintomas = [
        'Febre', 'DificuldadeRespiratoria', 'Tosse',
        'Coriza', 'DorGarganta', 'Diarreia', 'Cefaleia'
    ]

    resultado = {}

    for s in sintomas:
        resultado[s] = df.filter(col(s) == "Sim").count()

    pdf = pd.DataFrame(list(resultado.items()), columns=["Sintoma", "Quantidade"])
    pdf = pdf.sort_values("Quantidade", ascending=False)

    return pdf