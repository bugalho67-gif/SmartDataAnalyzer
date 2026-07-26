from sqlalchemy import create_engine


class DatabaseConnection:

    @staticmethod
    def sqlite(database):

        return create_engine(
            f"sqlite:///{database}"
        )

    @staticmethod
    def postgres(
        host,
        port,
        database,
        user,
        password
    ):

        return create_engine(

            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

        )

    @staticmethod
    def mysql(
        host,
        port,
        database,
        user,
        password
    ):

        return create_engine(

            f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

        )

    @staticmethod
    def sqlserver(
        host,
        database,
        user,
        password
    ):

        return create_engine(

            f"mssql+pyodbc://{user}:{password}@{host}/{database}?driver=ODBC+Driver+18+for+SQL+Server"

        )
