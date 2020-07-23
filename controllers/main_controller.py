import json

from flask import request

from json_objects import response_object
from connections import DatabaseConnect
from models import *


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

        return json.dumps({'123': '123'})
