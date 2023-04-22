import datetime
import sqlalchemy
from sqlalchemy import orm, Column, Integer, String, DateTime
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    task = orm.relationship("Task", back_populates='user')
