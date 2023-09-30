from data.admin import Admin
from data.InnerAPI.main_file import raise_error, check_params


def check_password(password):
    errors = {0: 'Пароль должен быть в длину 8 или более символов', 1: 'Пароль должен содержать хотя бы 1 букву',
              2: 'Пароль должен содержать хотя бы 1 цифру'}
    if not len(password) >= 8:
        return raise_error(errors[0])[0]
    if password.isdigit():
        return raise_error(errors[1])[0]
    if password.isalpha():
        return raise_error(errors[2])[0]
    return True


def get_admin(admin_email):
    admin, session = check_params(admin_email)
    if type(admin) is dict:
        return admin
    data = admin.to_dict()
    session.close()
    return data


def get_list_admin(admin_email):
    admin, session = check_params(admin_email)
    if type(admin) is dict:
        return admin
    admins = session.query(Admin).all()
    data = [item.to_dict() for item in admins]
    session.close()
    return data
