import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Target(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'target'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)                 # Название цели
    required_amount = sqlalchemy.Column(sqlalchemy.Float)       # Необходимая сумма
    collected_amount = sqlalchemy.Column(sqlalchemy.Float)      # Собранная сумма
    status = sqlalchemy.Column(sqlalchemy.Boolean)              # Статус цели

    company_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("company.id"))
    company = orm.relation('Company')

    def __repr__(self):
        return (f'<Target> Цель {self.name}, собранно {self.collected_amount} из {self.required_amount}, статус '
                f'{self.status}')
