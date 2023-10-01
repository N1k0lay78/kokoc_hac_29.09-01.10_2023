"""from data import db_session
from data.activity import Activity
from data.company import Company

db_session.global_init("db/kokos.sqlite")

session = db_session.create_session()
company = session.query(Company).get(1)
print(company)
activitis = [
    ["Отжимания", 100, "за 1 отжимание", "руки", 10],
    ["Приседания", 50, "за 1 приседание", "ноги", 10],
    ["Бег", 100, "за 1 км", "ноги", 10],
    ["Велосипед", 50, "за 1 км", "ноги", 10],
]
for name, coast, conventional_unit, type, base_count in activitis:
    activity = Activity()
    activity.name = name
    activity.coast = coast
    activity.conventional_unit = conventional_unit
    activity.type = type
    activity.base_count = base_count
    session.add(activity)
    session.commit()
session.close()
"""

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