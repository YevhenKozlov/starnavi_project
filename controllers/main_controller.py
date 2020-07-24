import json

from hashlib import md5
from flask import request
from sqlalchemy.orm import sessionmaker

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
            username = request.form['username']
            password = request.form['password']

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
            username = request.form['username']
            password = md5(request.form['password'].encode()).hexdigest()

            user = db_session.query(User).filter_by(username=username).one()
            if user.password != password:
                raise Exception('wrong password')

            result['data'] = {'access_token': user.get_token()}

        except Exception as e:
            result['success'] = False
            result['message'] = str(e)

        finally:
            db_session.close()

        return json.dumps(result, ensure_ascii=False)
