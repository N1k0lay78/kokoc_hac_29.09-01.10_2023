from sqlalchemy import and_

from data.InnerAPI.InnerTarget import find_target_by_id
from data.activity import Activity
from data.admin import Admin
from data.company import Company
from data.statistics import Statistics
from data.user import User
from data.InnerAPI.main_file import raise_error, check_params, check_user, check_company, check_email
from data import db_session


def find_by_id(id, session):
    user = session.query(User).get(id)
    if not user:
        return raise_error(f"Пользователь не найден", session)
    return user, session


def get_user(user_id):
    session = db_session.create_session()
    user, session = find_by_id(user_id, session)
    if type(user) is dict:
        session.close()
        return user
    data = user.to_dict(only=("id", "name", 'email', 'level', 'contribution', 'company_id', 'balance'))
    session.close()
    return data


def get_user_by_email(email):
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    if not user:
        session.close()
        return {"message": "Пользователь не найден"}
    data = user.to_dict(only=("id", "name", 'email', 'level', 'contribution', 'company_id', 'balance'))
    session.close()
    return data


def get_list_user():
    session = db_session.create_session()
    data = []
    for item in session.query(User).all():
        elem = item.to_dict(only=("id", "name", 'email', 'level', 'contribution', 'company_id', 'balance'))
        data.append(elem)
    session.close()
    return data


def put_user(email, args):
    user, session = check_user(email)
    if type(user) is dict:
        return user
    user_dict = user.to_dict(only=("name", 'email', 'level', 'balance'))
    keys = list(filter(lambda key: args[key] is not None and key in user_dict and args[key] != user_dict[key],
                       list(args.keys())))
    for key in keys:
        if key == 'name':
            user.name = args['name']
        if key == 'email':
            session = check_email(args["email"], session)
            if type(session) is dict:
                return session
            user.email = args['email']
        if key == 'level':
            user.level = args['level']
        if key == 'balance':
            user.balance = args['balance']
    if len(keys) == 0:
        return raise_error("Пустой запрос", session)[0]
    session.commit()
    session.close()
    return {"success": f"Успешно изменено"}


def delete_user(company_email, user_id):
    admin, session = check_company(company_email)
    if type(admin) is dict:
        return admin
    user, session = find_by_id(user_id, session)
    if type(user) is dict:
        return user
    for statistics in session.query(Statistics).filter(Statistics.user_id == user.id).all():
        session.delete(statistics)
    name = user.name
    session.delete(user)
    session.commit()
    session.close()
    return {"success": f"Пользователь {name} удалён"}


def create_user(company_unique_id, args):
    session = db_session.create_session()
    company = session.query(Company).filter(Company.unique_id == company_unique_id).first()
    if not company:
        return raise_error("Компания не найдена", session)

    company, session = check_company(company.email, args, ["name", 'email', 'level', 'password'])

    if type(company) is dict:
        return company

    session = check_email(args["email"], session)
    if type(session) is dict:
        return session

    new_user = User()
    new_user.name = args["name"]
    new_user.email = args["email"]
    new_user.level = args['level']
    new_user.contribution = 0
    new_user.balance = 0
    new_user.set_password(args['password'])
    new_user.company_id = company.id

    session.add(new_user)
    session.commit()
    id = new_user.id
    session.close()

    return {'id': id, 'success': f'Успешно зарегистрирован'}


def make_contribution(email, contribution, target_id):
    user, session = check_user(email)
    if type(user) is dict:
        return user

    target, session = find_target_by_id(target_id, session)
    if type(target) is dict:
        return target

    if user.balance < contribution:
        return raise_error("У вас недостаточно денег на балансе", session)

    if target.status:
        return raise_error("Эта цель уже достигнута", session)[0]

    need = target.required_amount - target.collected_amount
    if contribution > need:
        user.balance -= need
        target.collected_amount = target.required_amount
        target.status = True
        name = target.name
        session.commit()
        session.close()
        return {"success": f"Цель {name} достигнута!"}

    user.balance -= contribution
    target.collected_amount += contribution
    name = target.name
    need -= contribution
    session.commit()
    session.close()
    return {"success", f"Цель {name} стала ближе, до конца осталось {contribution}"}


def get_activity_statistics(user_email):
    user, session = check_user(user_email)
    if type(user) is dict:
        return user

    chart = []
    for activity in session.query(Statistics).filter(Statistics.user_id == user.id).all():
        dat = [0]
        try:
            for us in session.query(User).filter(User.company_id == user.company_id).all():
                stat = session.query(Statistics).filter(and_(Statistics.activity_id == activity.activity_id, Statistics.user_id == us.id)).first()
                if stat:
                    dat.append(sum([int(el2) for el2 in stat.history.split("/")[-7:]]) / 7)
                    print(dat)
            dat = sum(dat) / len(dat)
            dat2 = sum([int(el2) for el2 in activity.history.split("/")[-7:]]) / 7
            dat3 = [int(el2) for el2 in activity.history.split("/")[-7:]]
            dat3.extend([0] * (7 - len(dat3) if len(dat3) < 7 else 0))
            activity = session.query(Activity).filter(Activity.id == activity.activity_id).first()
            chart.append({
                "title": activity.name,
                "subtitle": activity.description,
                "avg_company": dat,
                "avg_user": dat2,
                "data": dat3
            })
        except Exception as e:
            print("#ZGBLJHFC!", e)
            pass
    session.close()
    return chart
