import sqlalchemy
from sqlalchemy import orm
from data.person import Person


class Company(Person):
    __tablename__ = 'Company'
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Person.id'), primary_key=True)
    unique_id = sqlalchemy.Column(sqlalchemy.String, unique=True)
    rates = sqlalchemy.Column(sqlalchemy.Float)
    logo = sqlalchemy.Column(sqlalchemy.String)

    users = orm.relation('User')
    targets = orm.relation('Target')

    def __repr__(self):
        return f'<Company> Компания {self.id} {self.name} {self.unique_id}'
