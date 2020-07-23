from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

from core.configs_wrapper import DatabaseConfig


class DatabaseConnect:
    """
    Class 'DatabaseConnect'
    Contain methods for connect to database (SQLALchemy)
    """

    @staticmethod
    def get_engine() -> Engine:
        """
        Getting object of Database engine

        :return: Engine, object of Database engine
        """

        config = DatabaseConfig()

        host = config.host
        port = int(config.port)
        username = config.username
        password = config.password
        db_name = config.db_name

        connection_string = f'postgres+psycopg2://{username}:{password}@{host}:{port}/{db_name}'
        engine = create_engine(connection_string)

        return engine
