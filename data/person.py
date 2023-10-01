import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from data.db_session import SqlAlchemyBase


class Person(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Person'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)

    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    __mapper_args__ = {
        'polymorphic_on': type,
    }

    def __repr__(self):
        return f'<Person> {self.id} Базовый юзер {self.name}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
