import datetime
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Move(SqlAlchemyBase):
    __tablename__ = 'move'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('game.id'), nullable=False)
    player = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    column = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

    def __repr__(self):
        return f'<Move> {self.id} {self.game_id} {self.player} {self.column}'
