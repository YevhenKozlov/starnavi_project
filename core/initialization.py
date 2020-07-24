from connections import DatabaseConnect
from models import *


class Initialization:
    """
    Class 'Initialization'
    Contain methods for initialization project
    """

    @staticmethod
    def database_initialization():
        """
        Database initialization method
        """

        # Initialization tables in database
        User.metadata.create_all(DatabaseConnect.get_engine())
        Post.metadata.create_all(DatabaseConnect.get_engine())
        Like.metadata.create_all(DatabaseConnect.get_engine())
