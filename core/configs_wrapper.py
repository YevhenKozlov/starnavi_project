from abc import ABC
from configparser import ConfigParser


class Config(ABC):
    """
    Abstract config class
    Encapsulation working with configs
    """

    def __setattr__(self, key: str, value: str):
        """
        Setter for update option configs
        Not create new option if not exist, only update existing

        :param key: str, option name
        :param value: str, data
        :return: None
        """

        # exception if type not string
        if type(value) != str:
            raise TypeError('Type must be str!')

        config = ConfigParser()
        config.read(self.path)

        # exception if not exist
        __ = config[self.section][key]

        config.set(self.section, key, value)

        with open(self.path, 'w') as config_file:
            config.write(config_file)

    def __getattr__(self, key: str) -> str:
        """
        Return option data

        :param key: str, option name
        :return: str, data from this option
        """

        config = ConfigParser()
        config.read(self.path)

        return config[self.section][key]

    def get_keys(self) -> list:
        """
        Getting all keys from selected config

        :return: list, collection keys from config
        """

        config = ConfigParser()
        config.read(self.path)

        return [item[0] for item in config.items(self.section)]


class MainConfig(Config):
    """
    Class 'MainConfig'

    Options:
        self.server_host - str, example 'localhost' or '0.0.0.0', etc...
        self.server_port - str, port {80 ... 65536}
        self.secret_key - str, Flask secret key

    Hints in PyCharm not worked
    """

    path = 'configs/main.ini'
    section = 'MAIN'


class DatabaseConfig(Config):
    """
    Class 'DatabaseConfig'

    Options:
        self.db_name - str, name of PostgreSQL database
        self.username - str, username for database
        self.password - str, password for database
        self.host - str, example 'localhost' or '0.0.0.0', etc...
        self.port - str, port {80 ... 65536}

    Hints in PyCharm not worked
    """

    path = 'configs/main.ini'
    section = 'DATABASE'
