from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .users import Base


class Post(Base):
    """
    Model for table 'posts'
    """

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow(), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    likes = relationship('Like')

    def __init__(self, title: str, text: str, user_id: int):
        """
        Constructor for create new item in this table

        :param title: str, title of post
        :param text: str, text of post
        :param user_id: int, user identity
        """

        self.title = title
        self.text = text
        self.user_id = user_id
