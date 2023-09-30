import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    level = sqlalchemy.Column(sqlalchemy.String)            # Уровень подготовки
    hashed_password = sqlalchemy.Column(sqlalchemy.String)

    company_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("company.id"))
    company = orm.relation('Company')

    # company = orm.relation('Company')
    # admin_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("admin.id"))
    # admin = orm.relation('Admin')

    def __repr__(self):
        return f'<User> Пользователь {self.id} {self.name} {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)