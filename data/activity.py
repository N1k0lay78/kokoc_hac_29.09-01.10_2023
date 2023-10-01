import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Activity(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Activity'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    coast = sqlalchemy.Column(sqlalchemy.Integer)        # Стоимость за 1 условную единицу упражнения
    conventional_unit = sqlalchemy.Column(sqlalchemy.String)        # Условная единица
    type = sqlalchemy.Column(sqlalchemy.String)         # Тип упражнения (какую группу мышц качает)
    description = sqlalchemy.Column(sqlalchemy.String)         # Описание
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)         # Картинка
    base_count = sqlalchemy.Column(sqlalchemy.Integer)   # Базовое количество выполняемых условных единиц, кол-во необходимых равно level * base_count

    statistics = orm.relation('Statistics')

    def __repr__(self):
        return f'<Activity> Активность {self.name}, за {self.conventional_unit} платят {self.coast}'
