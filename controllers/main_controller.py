import json

from datetime import datetime
from hashlib import md5
from flask import request
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    @jwt_required
    def create_post():
        """
        Creating new post
        """

        user_id = get_jwt_identity()

        result = response_object.copy()
        db_session = DatabaseSession()

        try:
            new_post = Post(
                title=request.form['title'],
                text=request.form['text'],
                user_id=user_id,
                timestamp=datetime.fromtimestamp(request.form['timestamp'])
            )

            db_session.add(new_post)
            db_session.commit()

        except Exception as e:
            result['success'] = False
            result['message'] = str(e)

        finally:
            db_session.close()

        return json.dumps(result, ensure_ascii=False)

    @staticmethod
    @jwt_required
    def like_post():
        """
        Save like
        """

        user_id = get_jwt_identity()

        result = response_object.copy()
        db_session = DatabaseSession()

        try:
            new_like = Like(
                user_id=user_id,
                post_id=request.form['post_id'],
                timestamp=datetime.fromtimestamp(request.form['timestamp']),
                type_=True
            )

            db_session.add(new_like)
            db_session.commit()

        except Exception as e:
            result['success'] = False
            result['message'] = str(e)

        finally:
            db_session.close()

        return json.dumps(result, ensure_ascii=False)

    @staticmethod
    @jwt_required
    def unlike_post():
        """
        Save unlike
        """

        user_id = get_jwt_identity()

        result = response_object.copy()
        db_session = DatabaseSession()

        try:
            new_like = Like(
                user_id=user_id,
                post_id=request.form['post_id'],
                timestamp=datetime.fromtimestamp(request.form['timestamp']),
                type_=False
            )

            db_session.add(new_like)
            db_session.commit()

        except Exception as e:
            result['success'] = False
            result['message'] = str(e)

        finally:
            db_session.close()

        return json.dumps(result, ensure_ascii=False)

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

            response_last_login_time = str(last_login_time) if last_login_time else None
            response_last_action_time = str(last_action_time) if last_action_time else None

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
            # TODO: Need write this method
            # query = db_session.query(Post, Like)\
            #     .filter(Post.id == Like.post_id)\
            #     .filter(Like.timestamp >= date_from)\
            #     .filter(Like.timestamp <= date_to)\
            #     .all()
            #
            # result_posts_list = list()
            # for post in query:
            #     package = {
            #         'id': post.id,
            #         'number_of_likes': len(),
            #         'number_of_unlikes': len()
            #     }
            #     result_posts_list.append(package)
            #
            # result['data'] = {
            #     'posts': result_posts_list
            # }

            pass

        except Exception as e:
            result['success'] = False
            result['message'] = str(e)

        finally:
            db_session.close()

        return json.dumps(result, ensure_ascii=False)
