import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Statistics(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'statistics'
    history = sqlalchemy.Column(sqlalchemy.String)      # Отчёт по кол-ву в день 10/42/0/0/0/0/12/42/15
    start_date = sqlalchemy.Column(sqlalchemy.String)   # Дата, когда начали вести отчёт по этой активности
    all = sqlalchemy.Column(sqlalchemy.Integer)         # Сколько сделали за всё время

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = orm.relation('User')

    activity_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Activity.id"))
    activity = orm.relation('Activity')

    def __repr__(self):
        return f'<Statistics> Статистика пользователя {self.user_id} по активности {self.activity_id}'
