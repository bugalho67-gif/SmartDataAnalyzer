import pandas as pd


def execute_query(engine, sql):

    return pd.read_sql(
        sql,
        engine
    )


def list_tables(engine):

    consulta = """

    SELECT table_name

    FROM information_schema.tables

    WHERE table_schema='public'

    """

    return pd.read_sql(
        consulta,
        engine
    )
