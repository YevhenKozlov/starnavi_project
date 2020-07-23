import json

from hashlib import md5
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
        db_session = DatabaseSession()

        try:
            username = json.loads(request.form['username'])
            password = json.loads(request.form['password'])

            new_user = User(username, password)
            db_session.add(new_user)
            db_session.commit()

        except Exception as e:
            result['success'] = False
            result['message'] = str(e)

        finally:
            db_session.close()

        return json.dumps(result, ensure_ascii=False)

    @staticmethod
    def login():
        """
        User login in system
        Return token
        """

        result = response_object.copy()
        db_session = DatabaseSession()

        try:
            username = json.loads(request.form['username'])
            password = json.loads(request.form['password'])
            password_hash = md5(password.encode()).hexdigest()

            db_session = DatabaseSession()
            users = db_session.query(User).filter_by(username=username, password=password_hash)

            if users.count() == 1:
                session_token = SessionManager.new_session(users[0].id)
                result['data'] = session_token

            else:
                raise Exception('user not found')

        except Exception as e:
            result['success'] = False
            result['message'] = str(e)

        finally:
            db_session.close()

        return json.dumps(result, ensure_ascii=False)
