from hashlib import md5
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """
    Model for table 'users'
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    last_login_time = Column(DateTime(timezone=True))

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
