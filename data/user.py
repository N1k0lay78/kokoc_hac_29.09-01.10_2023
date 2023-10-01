import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    level = sqlalchemy.Column(sqlalchemy.Integer)           # Уровень подготовки
    contribution = sqlalchemy.Column(sqlalchemy.Float)      # Вклад за всё время
    balance = sqlalchemy.Column(sqlalchemy.Float)           # Вклад за всё время
    hashed_password = sqlalchemy.Column(sqlalchemy.String)

    company_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("company.id"))
    company = orm.relationship('Company', back_populates="user")

    statistics = orm.relation('Statistics')

    def __repr__(self):
        return f'<User> Пользователь {self.id} {self.name} {self.email}, с уровнем {self.level}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
