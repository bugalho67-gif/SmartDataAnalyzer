def recommendations(df):

    dicas = []

    if df.isnull().sum().sum() > 0:

        dicas.append(

            "Existem valores nulos."

        )

    if df.duplicated().sum() > 0:

        dicas.append(

            "Existem registros duplicados."

        )

    return dicas
