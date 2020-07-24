from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime

from .users import Base


class Like(Base):
    """
    Model for table 'likes'
    """

    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    type = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __init__(self, user_id: int, post_id: int, type_: bool, timestamp: datetime = datetime.now()):
        """
        Constructor for create new item in this table

        :param user_id: int, user identity
        :param post_id: int, post identity
        :param type_: bool, type of mark (0 - dislike, 1 - like)
        :param timestamp: datetime, time of create new like (default = now)
        """

        self.user_id = user_id
        self.post_id = post_id
        self.type = type_
        self.timestamp = timestamp
