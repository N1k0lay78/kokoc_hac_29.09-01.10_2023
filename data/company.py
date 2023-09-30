import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from data.db_session import SqlAlchemyBase


class Company(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'company'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    unique_id = sqlalchemy.Column(sqlalchemy.String, unique=True)
    rates = sqlalchemy.Column(sqlalchemy.Float, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)

    users = orm.relation('User')
    targets = orm.relation('Target')

    def __repr__(self):
        return f'<Company> Компания {self.id} {self.name} {self.unique_id}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
