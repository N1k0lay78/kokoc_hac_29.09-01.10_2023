from data.admin import Admin
from data import db_session
from data.company import Company
from data.user import User


def raise_error(error, session=None):
    if session:
        session.close()
    return {"message": error}, 1


def check_admin_status(email, need_status=1):
    admin, session = check_admin(email)
    if type(admin) is dict:
        return admin, session
    if admin.status < int(need_status):
        return raise_error("У вас недостаточно прав для этого", session)
    return admin, session


def check_admin(email_admin):
    session = db_session.create_session()
    user = session.query(Admin).filter(Admin.email == email_admin).first()
    if not user:
        return raise_error(f"Админ {email_admin} не найден", session)
    return user, session


def check_company(email_company, args=None, params=None):
    session = db_session.create_session()
    company = session.query(Company).filter(Company.email == email_company).first()
    if not company:
        return raise_error(f"Компания {email_company} не найдена", session)
    if params:
        if not all(key in args and args[key] is not None for key in params):
            return raise_error(f"Отсутствуют важные параметры: {params}")
    return company, session


def check_user(email_user, args=None, params=None):
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email_user).first()
    if not user:
        return raise_error(f"Пользователь {email_user} не найден", session)
    if params:
        if not all(key in args and args[key] is not None for key in params):
            return raise_error(f"Отсутствуют важные параметры: {params}")
    return user, session


def check_params(admin_email, args=None, params=None, status=0):
    if params is not None:
        if not all(key in args and args[key] is not None for key in params):
            return raise_error(f"Отсутствуют важные параметры: {params}")
    return check_admin_status(admin_email, status)
