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
    def registration():
        """
        User registration
        """

        result = response_object.copy()

        try:
            username = json.loads(request.form['username'])
            password = json.loads(request.form['password'])

            db_session = DatabaseSession()
            new_user = User(username, password)
            db_session.add(new_user)
            db_session.commit()

        except Exception as e:
            result['success'] = False
            result['message'] = str(e)

        return json.dumps(result, ensure_ascii=False)
