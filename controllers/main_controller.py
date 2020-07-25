import json
import time

from datetime import datetime
from hashlib import md5
from flask import request
from sqlalchemy import func
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

            user.last_login_time = datetime.fromtimestamp(time.time())
            db_session.add(user)
            db_session.commit()

        except Exception as e:
            result['success'] = False
            result['message'] = str(e)

        finally:
            db_session.close()

        return json.dumps(result, ensure_ascii=False), 200 if result['success'] else 401

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
            print(request.form)
            new_post = Post(
                title=request.form['title'],
                text=request.form['text'],
                user_id=user_id,
                timestamp=datetime.fromtimestamp(int(request.form['timestamp']))
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
                timestamp=datetime.fromtimestamp(int(request.form['timestamp'])),
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
    def dislike_post():
        """
        Save dislike
        """

        user_id = get_jwt_identity()

        result = response_object.copy()
        db_session = DatabaseSession()

        try:
            new_dislike = Like(
                user_id=int(user_id),
                post_id=request.form['post_id'],
                timestamp=datetime.fromtimestamp(int(request.form['timestamp'])),
                type_=False
            )

            db_session.add(new_dislike)
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
            analytics_data = dict()

            # 0 - dislikes, 1 - likes
            for like_type in ['0', '1']:
                query_result = db_session.query(Post, func.count(Like.id))\
                    .join(Like, Post.id == Like.post_id)\
                    .filter(Like.timestamp >= date_from)\
                    .filter(Like.timestamp <= date_to)\
                    .filter(Like.type == like_type)\
                    .group_by(Post.id).all()

                for item in query_result:

                    package = {
                        'number_of_likes': 0,
                        'number_of_dislikes': 0
                    }

                    key = 'number_of_likes' if like_type == '1' else 'number_of_dislikes'

                    if item[0].id not in analytics_data.keys():
                        package[key] = item[1]
                        analytics_data[item[0].id] = package

                    else:
                        analytics_data[item[0].id][key] = item[1]

            result['data'] = {
                'posts': analytics_data
            }

        except Exception as e:
            result['success'] = False
            result['message'] = str(e)

        finally:
            db_session.close()

        return json.dumps(result, ensure_ascii=False)
