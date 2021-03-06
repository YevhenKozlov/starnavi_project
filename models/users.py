from time import mktime
from hashlib import md5
from datetime import timedelta, datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token

Base = declarative_base()


class User(Base):
    """
    Model for table 'users'
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    last_login_time = Column(DateTime)

    posts = relationship('Post')
    likes = relationship('Like')

    def __init__(self, username: str, password: str):
        """
        Constructor for create new item in this table

        :param username: str, user nick-name
        :param password: str, user password (automatically hashed to md5)
        """

        self.username = username
        self.password = md5(password.encode()).hexdigest()

    def get_last_action_time(self) -> datetime or None:
        """
        Method for getting last action time

        :return: datetime, timestamp (return None if action not found)
        """

        max_timestamp = 0

        for post in self.posts:
            timestamp = mktime(post.timestamp.timetuple())
            if timestamp > max_timestamp:
                max_timestamp = timestamp

        for like in self.likes:
            timestamp = mktime(like.timestamp.timetuple())
            if timestamp > max_timestamp:
                max_timestamp = timestamp

        return datetime.fromtimestamp(max_timestamp) if max_timestamp else None

    def get_token(self, expire_time: int = 24) -> str:
        """
        Getting JWT token

        :param expire_time: int, token expire time (default = 24 hours)
        :return: str, token
        """

        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)

        return token
