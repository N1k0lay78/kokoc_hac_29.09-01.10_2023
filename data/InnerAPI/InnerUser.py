from data.user import User
from data.statistics import Statistics
from data.user import User
from data.target import Target
from data.InnerAPI.main_file import raise_error, check_params, check_user
from data import db_session


def find_by_id(id, session):
    user = session.query(User).get(id)
    if not user:
        return raise_error(f"Пользователь не найден не найдена", session)
    return user, session


def get_user(user_id):
    session = db_session.create_session()
    user, session = find_by_id(user_id, session)
    if type(user) is dict:
        session.close()
        return user
    data = user.to_dict(only=("id", "name", 'email', 'unique_id', 'rates', 'logo'))
    session.close()
    return data


def get_user_by_name(name):
    session = db_session.create_session()
    user = session.query(User).filter(User.name == name).first()
    if not user:
        session.close()
        return {"message": "Компания не найдена не найден"}
    data = user.to_dict(only=("id", "name", 'email', 'unique_id', 'rates', 'logo'))
    session.close()
    return data


def get_list_user():
    session = db_session.create_session()
    data = []
    for item in session.query(User).all():
        elem = item.to_dict(only=("id", "name", 'email', 'unique_id', 'rates', 'logo'))
        data.append(elem)
    session.close()
    return data


def put_user(email, args):
    user, session = check_user(email)
    if type(user) is dict:
        return user
    user_dict = user.to_dict(only=("name", 'email', 'rates', 'logo'))
    keys = list(filter(lambda key: args[key] is not None and key in user_dict and args[key] != user_dict[key],
                       list(args.keys())))
    for key in keys:
        if key == 'name':
            if session.query(User).filter(User.name == args["name"]).first():
                return raise_error("Это название уже занято", session)[0]
            user.name = args['name']
        if key == 'email':
            if session.query(User).filter(User.email == args["email"]).first():
                return raise_error("Эта почта уже занято", session)[0]
            user.email = args['email']
        if key == 'rates':
            user.rates = args['rates']
        if key == 'logo':
            user.logo = args['logo']
    if len(keys) == 0:
        return raise_error("Пустой запрос", session)[0]
    session.commit()
    session.close()
    return {"success": f"Успешно изменено"}


def delete_user(admin_email, user_id):
    admin, session = check_params(admin_email)
    if type(admin) is dict:
        return admin
    user, session = find_by_id(user_id, session)
    if type(user) is dict:
        return user
    for user in session.query(User).filter(User.user_id == user_id).all():
        for statistics in session.query(Statistics).filter(Statistics.user_id == user.id).all():
            session.delete(statistics)
        session.delete(user)
    for target in session.query(Target).filter(Target.user_id == user_id).all():
        session.delete(target)
    name = user.name
    session.delete(user)
    session.commit()
    session.close()
    return {"success": f"Компания {name} удалена"}


def create_user(admin_email, args):
    admin, session = check_params(admin_email, args, ["name", 'email', 'rates', 'logo'])

    if type(admin) is dict:
        return admin

    new_user = User()
    new_user.name = args["name"]
    new_user.email = args["email"]
    while True:
        unique_id = "".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
                             for i in range(64)])
        if not session.query(User).filter(User.unique_id == unique_id).first():
            break
    new_user.unique_id = args['unique_id']
    new_user.rates = args['rates']
    new_user.logo = args['logo']

    session.add(new_user)
    session.commit()
    id = new_user.id
    session.close()

    return {'id': id, 'success': f'Компания создана {args["name"]} создан'}
