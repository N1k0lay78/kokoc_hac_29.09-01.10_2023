import sqlalchemy
from sqlalchemy import orm
from data.person import Person


class User(Person):
    __tablename__ = 'User'
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Person.id'), primary_key=True)
    level = sqlalchemy.Column(sqlalchemy.Integer)           # Уровень подготовки
    contribution = sqlalchemy.Column(sqlalchemy.Float)      # Вклад за всё время
    balance = sqlalchemy.Column(sqlalchemy.Float)           # Вклад за всё время

    company_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Company.id"))
    company = orm.relation('Company')

    statistics = orm.relation('Statistics')

    def __repr__(self):
        return f'<User> Пользователь {self.id} {self.name} {self.email}, с уровнем {self.level}'
