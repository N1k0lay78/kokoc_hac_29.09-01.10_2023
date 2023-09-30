import random
from data.company import Company
from data.statistics import Statistics
from data.user import User
from data.target import Target
from data.InnerAPI.main_file import raise_error, check_params, check_company
from data import db_session


def find_by_id(id, session):
    company = session.query(Company).get(id)
    if not company:
        return raise_error(f"Компания не найдена", session)
    return company, session


def get_company(company_id):
    session = db_session.create_session()
    company, session = find_by_id(company_id, session)
    if type(company) is dict:
        session.close()
        return company
    data = company.to_dict(only=("id", "name", 'email', 'unique_id', 'rates', 'logo'))
    session.close()
    return data


def get_company_by_name(name):
    session = db_session.create_session()
    company = session.query(Company).filter(Company.name == name).first()
    if not company:
        session.close()
        return {"message": "Компания не найдена"}
    data = company.to_dict(only=("id", "name", 'email', 'unique_id', 'rates', 'logo'))
    session.close()
    return data


def get_list_company():
    session = db_session.create_session()
    data = []
    for item in session.query(Company).all():
        elem = item.to_dict(only=("id", "name", 'email', 'unique_id', 'rates', 'logo'))
        data.append(elem)
    session.close()
    return data


def put_company(email, args):
    company, session = check_company(email)
    if type(company) is dict:
        return company
    company_dict = company.to_dict(only=("name", 'email', 'rates', 'logo'))
    keys = list(filter(lambda key: args[key] is not None and key in company_dict and args[key] != company_dict[key],
                       list(args.keys())))
    for key in keys:
        if key == 'name':
            if session.query(Company).filter(Company.name == args["name"]).first():
                return raise_error("Это название уже занято", session)[0]
            company.name = args['name']
        if key == 'email':
            if session.query(Company).filter(Company.email == args["email"]).first():
                return raise_error("Эта почта уже занято", session)[0]
            company.email = args['email']
        if key == 'rates':
            company.rates = args['rates']
        if key == 'logo':
            company.logo = args['logo']
    if len(keys) == 0:
        return raise_error("Пустой запрос", session)[0]
    session.commit()
    session.close()
    return {"success": f"Успешно изменено"}


def delete_company(admin_email, company_id):
    admin, session = check_params(admin_email)
    if type(admin) is dict:
        return admin
    company, session = find_by_id(company_id, session)
    if type(company) is dict:
        return company
    for user in session.query(User).filter(User.company_id == company_id).all():
        for statistics in session.query(Statistics).filter(Statistics.user_id == user.id).all():
            session.delete(statistics)
        session.delete(user)
    for target in session.query(Target).filter(Target.company_id == company_id).all():
        session.delete(target)
    name = company.name
    session.delete(company)
    session.commit()
    session.close()
    return {"success": f"Компания {name} удалена"}


def create_company(admin_email, args):
    admin, session = check_params(admin_email, args, ["name", 'email', 'rates', 'logo', 'password'])

    if type(admin) is dict:
        return admin

    new_company = Company()
    new_company.name = args["name"]
    new_company.email = args["email"]
    while True:
        unique_id = "".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
                             for i in range(64)])
        if not session.query(Company).filter(Company.unique_id == unique_id).first():
            break
    new_company.unique_id = args['unique_id']
    new_company.rates = args['rates']
    new_company.logo = args['logo']
    new_company.set_password(args['password'])

    session.add(new_company)
    session.commit()
    id = new_company.id
    session.close()

    return {'id': id, 'success': f'Компания создана {args["name"]} создан'}
