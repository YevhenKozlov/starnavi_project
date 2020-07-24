import json

from hashlib import md5
from flask import request
from datetime import datetime
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
        Return access token
        """

        result = response_object.copy()
        db_session = DatabaseSession()

        try:
            username = request.form['username']
            password = md5(request.form['password'].encode()).hexdigest()

            user = db_session.query(User).filter_by(username=username).one()
            if user.password != password:
                raise Exception('wrong password')

            result['data'] = {
                'access_token': user.get_token()
            }

        except Exception as e:
            result['success'] = False
            result['message'] = str(e)

        finally:
            db_session.close()

        return json.dumps(result, ensure_ascii=False)

    @staticmethod
    def create_post():
        """
        Creating new post
        """

        # TODO: Need write this method

        pass

    @staticmethod
    def like_post():
        """
        Save like
        """

        # TODO: Need write this method

        pass

    @staticmethod
    def unlike_post():
        """
        Save unlike
        """

        # TODO: Need write this method

        pass

    @staticmethod
    def user_activity(user_id: int):
        """
        Getting last login time in system & last action time
        """

        result = response_object.copy()
        db_session = DatabaseSession()

        try:
            user = db_session.query(User).filter_by(id=user_id).one()

            last_login_time = user.last_login_time
            last_action_time = user.get_last_action_time()

            response_last_login_time = str(last_login_time).split(' ')[0] if last_login_time else None
            response_last_action_time = str(last_action_time).split(' ')[0] if last_action_time else None

            result['data'] = {
                'last_login_time': response_last_login_time,
                'last_action_time': response_last_action_time,
            }

        except Exception as e:
            result['success'] = False
            result['message'] = str(e)

        finally:
            db_session.close()

        return json.dumps(result, ensure_ascii=False)

    @staticmethod
    def analytics(date_from: str, date_to: str):
        """
        Getting analytics likes|unlikes by date range
        """

        result = response_object.copy()
        db_session = DatabaseSession()

        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d')
            date_to = datetime.strptime(date_to, '%Y-%m-%d')

            # TODO: query to DB

        except Exception as e:
            result['success'] = False
            result['message'] = str(e)

        finally:
            db_session.close()

        return json.dumps(result, ensure_ascii=False)
