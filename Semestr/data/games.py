import datetime
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = 'game'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'))
    moves = orm.relationship('Move', backref='game', lazy=True)

    def __repr__(self):
        return f'<Game> {self.id} {self.user_id}'
