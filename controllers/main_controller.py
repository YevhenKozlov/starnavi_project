import json

from flask import request
from sqlalchemy.orm import sessionmaker

from core import SessionManager
from json_objects import response_object
from connections import DatabaseConnect
from models import *

DatabaseSession = sessionmaker(bind=DatabaseConnect.get_engine())


class MainController:
    """
    Class 'MainController'
    Contains all controller-methods
    """

    @staticmethod
    def test():
        """
        TEST
        """

        SessionManager.new_session(123)

        return json.dumps({'123': '123'})
