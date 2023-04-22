import datetime
import sqlalchemy
from sqlalchemy import orm, Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
#    created_date = Column(DateTime, default=datetime.datetime.now)
    execution_time = Column(String, default='не засечено')
    is_completed = Column(Boolean, default=False)
    start_time = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = orm.relationship('User')
