import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Activity(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'activity'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    coast = sqlalchemy.Column(sqlalchemy.String)        # Стоимость за 1 условную единицу упражнения
    type = sqlalchemy.Column(sqlalchemy.String)         # Тип упражнения (какую группу мышц качает)

    statistics = orm.relation('Statistics')

    admin_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Admin.id"))
    admin = orm.relation('Admin')

    def __repr__(self):
        return f'<Activity> Активность {self.name}'
