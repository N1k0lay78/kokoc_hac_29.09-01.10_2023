from data import db_session
from data.activity import Activity
from data.company import Company
from data.user import User
from data.statistics import Statistics
from data.InnerAPI.InnerStatistics import create_statistics

db_session.global_init("db/kokos.sqlite")

session = db_session.create_session()
for us in session.query(User).all():
    for i in range(1, 5):
        print(create_statistics(us.email, i))

session.close()