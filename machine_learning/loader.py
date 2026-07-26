import pandas as pd
from pathlib import Path


class DataLoader:

    @staticmethod
    def load(file):

        extension = Path(file.name).suffix.lower()

        if extension == ".csv":
            return pd.read_csv(file)

        elif extension == ".xlsx":
            return pd.read_excel(file)

        elif extension == ".json":
            return pd.read_json(file)

        else:
            raise ValueError(
                f"Formato {extension} não suportado."
            )
