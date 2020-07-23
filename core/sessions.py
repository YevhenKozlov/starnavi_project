import random
import string

from connections import RedisConnect


class SessionManager:
    """
    Class 'SessionManager'
    This class contain methods for manage sessions
    """

    @staticmethod
    def new_session(user_id: int) -> str:
        """
        Create new session, save to Redis

        :param user_id: int, user identity
        :return: str, unique token for session
        """

        redis = RedisConnect()
        SessionManager.drop_session(user_id)

        while True:
            token = ''.join(random.choice(string.ascii_lowercase) for __ in range(64))

            for session_name in redis.connection.keys():
                if redis.connection.get(session_name).decode() == token:
                    continue
            break

        redis.connection.set(f'session_{user_id}', token)
        redis.connection.expire(f'session_{user_id}', 1800)

        return token

    @staticmethod
    def drop_session(user_id: int):
        """
        Drop concrete user session

        :param user_id: int, user identity
        """

        redis = RedisConnect()

        if SessionManager.exists(user_id):
            redis.connection.delete(f'session_{user_id}')

    @staticmethod
    def drop_all_session():
        """
        Drop all user sessions
        """

        redis = RedisConnect()
        redis.connection.flushdb()

    @staticmethod
    def exists(user_id: int) -> bool:
        """
        Check existing session for concrete user

        :param user_id: int, user identity
        :return: bool, check result
        """

        redis = RedisConnect()
        return redis.connection.exists(f'session_{user_id}')

    @staticmethod
    def get_user_id(token: str) -> int or None:
        """
        Getting user identity

        :param token: str, unique session-token
        :return: int, user identity or None if not found
        """

        redis = RedisConnect()

        for session_name in redis.connection.keys():
            if token == redis.connection.get(session_name).decode():
                return int(session_name.decode().split('_')[-1])

        return None
