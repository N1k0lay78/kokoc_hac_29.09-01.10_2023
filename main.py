import os
import random

import jsonpickle
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
import config
from data import db_session
from data.InnerAPI.InnerCompany import create_company
from data.InnerAPI.InnerStatistics import put_statistics
from data.InnerAPI.InnerTarget import create_target, delete_target
from data.InnerAPI.InnerUser import create_user, make_contribution
from data.InnerAPI.InnerUser import get_activity_statistics
from data.activity import Activity
from data.admin import Admin
from data.company import Company
from data.forms import FormLogin, FormUserRegistration, FormCompanyRegistration, FormFondEdit, FormFondCreate, \
    FormFondDelete, FormFondAdd, FormFondRemove, FormMakeWork, FormMakePay
from data.target import Target
from data.user import User

mail = None

application = Flask(__name__)
db_session.global_init("db/kokos.sqlite")
application.config.from_object(config)
login_manager = LoginManager()
login_manager.init_app(application)


def create_random_name(name_len):
    let = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    return ''.join([random.choice(let) for i in range(name_len)])


def create_new_image_name():
    filelist, format = os.listdir(application.config['UPLOAD_FOLDER']), ".png"
    filename = create_random_name(50) + format
    while filename in filelist:
        filename = create_random_name(50) + format
    return filename


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    session = db_session.create_session()
    user = session.query(Admin).filter(Admin.email == user_id).first()
    if not user:
        user = session.query(User).filter(User.email == user_id).first()
        if not user:
            user = session.query(Company).filter(Company.email == user_id).first()
    session.close()
    return user


def my_render(filename, **kwargs):
    my_kwargs = {
        "need_log": True,
        "is_authorized": not current_user.is_anonymous,
        "is_logout": False,
        "user_id": current_user.id if not current_user.is_anonymous else -1,
    }
    for key, val in kwargs.items():
        my_kwargs[key] = val
    return render_template(filename, **my_kwargs)


@application.route("/")
def main_page():
    return my_render("base.html", title="Главная страница")


@application.route("/login/", methods=["GET", "POST"])
def login_page():
    global mail
    if not current_user.is_anonymous:
        return redirect("/")
    form = FormLogin()
    if request.method == "POST":
        session = db_session.create_session()
        person = session.query(User).filter(User.email == form.email.data).first()
        if not person:
            person = session.query(Company).filter(Company.email == form.email.data).first()
            if not person:
                person = session.query(Admin).filter(Admin.email == form.email.data).first()
        if person:
            person.id = person.email
        session.close()
        if person and person.check_password(form.password.data):
            mail = form.email.data
            login_user(person, remember=False)
            return redirect("/")  # если успех
        return redirect("/")  # если неуспех
    return my_render("login.html", title="Авторизация", need_log=False, form=form)


@application.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/")


@application.route("/user/registration/<string:code>/", methods=["GET", "POST"])
def user_registration_page(code):  # /user/registration/5zbFscdWU7NUUSFBjzA9UlFnUaUTUHx8HK7ybNjk7dL7xHWzGmO4wqUgeaP8qnjU
    form = FormUserRegistration()
    message, result = None, False
    if request.method == 'POST':
        if form.password_1.data == form.password_2.data:
            message = create_user(code, {"name": form.name.data, "email": form.email.data, "level": form.level.data,
                                         "password": form.password_1.data})
            if "success" in message:
                return redirect("/login")
            message = list(message.values())[-1]
        else:
            message = "Пароли не совпадают"
    return my_render('user-registration.html', title="Регистрация", message=message, form=form, result=result)


@application.route("/user/activity/<string:email>")
def user_activity(email):
    data = get_activity_statistics(email)
    print(email)
    return jsonpickle.encode(data)

# TELEPORT
@application.route("/user/profile/<int:id>/")
def user_profil_page(id):
    sessia = db_session.create_session()
    fonds = sessia.query(Target).filter(Target.company_id == current_user.company_id).all()
    users = sessia.query(User).filter(User.company_id == current_user.company_id).order_by(-User.balance).all()
    user = sessia.query(User).get(id)
    sessia.close()
    if not user:
        return redirect("/")
    return my_render("user-profile.html", is_authorized=True, is_logout=True, coast=user.balance, users=users,
                     user_email=user.email, fonds=fonds, user=user)


@application.route("/user/work/")
def user_work():
    if current_user.is_anonymous:
        return redirect("/")
    session = db_session.create_session()
    acts = session.query(Activity).all()
    types = set()
    for act in acts:
        types.add(act.type)
    types = list(types)
    return my_render("user-work.html", types=types, acts=acts, current_user=current_user)


@application.route("/user/make_work/<int:id>", methods=["GET", "POST"])
def user_make_work(id):
    if current_user.is_anonymous:
        return redirect("/")
    form = FormMakeWork()
    if request.method == 'POST':
        put_statistics(current_user.email, id, form.count.data)
        return redirect("/")
    session = db_session.create_session()
    acts = session.query(Activity).get(id)
    session.close()
    return my_render('user-make-work.html', title="Записать количество", form=form, name=acts.name)



@application.route("/user/fonds/")
def user_fonds():
    sessia = db_session.create_session()
    fonds = sessia.query(Target).filter(Target.company_id == current_user.company_id).all()
    sessia.close()
    return my_render("user-fonds.html", fonds=fonds)


@application.route("/fond/spend/<int:id>", methods=["GET", "POST"])
def fond_spend_page(id):
    form = FormMakePay()
    err = ""
    if request.method == 'POST':
        resp = make_contribution(current_user.email, form.count.data, id)
        if "success" in resp:
            return redirect("/")
        else:
            err = resp["message"]
    sessia = db_session.create_session()
    fond = sessia.query(Target).get(id)
    sessia.close()
    return my_render("fond-spend.html", form=form, name=fond.name, message=err, result=False)


@application.route("/fond/add/<int:id>")
def fond_add(id):
    # TODO:
    form = FormFondAdd()
    name = f"Фонд №{id}"
    return my_render("fond-add.html", name=name, form=form)


@application.route("/fond/remove/<int:id>")
def fond_remove(id):
    form = FormFondRemove()
    name = f"Фонд №{id}"
    return my_render("fond-remove.html", name=name, form=form)


@application.route("/company/registration", methods=["GET", "POST"])
def company_registration_page():
    form = FormCompanyRegistration()
    message, result = None, False
    if request.method == 'POST':
        if form.password_1.data == form.password_2.data:
            message = create_company({"name": form.name.data, "email": form.email.data, "rates": form.rates.data,
                                      "logo": "./static/img/kokoc_logo.png", "password": form.password_1.data})
            if "success" in message:
                return redirect("/login")
            message = list(message.values())[-1]
        else:
            message = "Пароли не совпадают"
    return my_render('company-registration.html', title="Регистрация", message=message, form=form, result=result)


@application.route("/company/<int:id>/")
def company_page(id):
    leaderboard = [
        ["Rjkzavr", 56262.36, 1],
        ["Nikniksham", 56262.36, 2],
        ["Niki", 56262.36, 3],
        ["Juk", 56262.36, 4],
        ["Rjkz", 56262.36, 5],
        ["NikTV_78", 56262.36, 6],
        ["bobr", 56262.36, 7],
        ["kaiga", 56262.36, 8],
        ["dragon", 56262.36, 9],
        ["itv", 56262.36, 10],
        ["Cha Cha", 56262.36, 11],
        ["turtle", 56262.36, 12],
    ]
    # TODO:
    # Сделать страницу компании (добавить иконку, название, фонды и графики)
    return my_render("company.html", title="Страница компании", leaderboard=leaderboard)


@application.route("/company/profile/<int:id>/")
# TELEPORT
def company_profile_page(id):
    sessia = db_session.create_session()
    fonds = sessia.query(Target).filter(Target.company_id == id).all()
    users = sessia.query(User).filter(User.company_id == id).order_by(-User.balance).all()
    sessia.close()

    return my_render("company-profile.html", title="Профиль", is_logout=True, is_authorized=True,
                     users=users, fonds=fonds)


@application.route("/company/edit/", methods=["POST", "GET"])
def company_edit():
    # необязательно
    return redirect("/company/profile/123")


@application.route("/delte/user/<int:id>", methods=["POST", "GET"])
def delete_user():
    # необязательно
    return redirect("/company/profile/123")


@application.route("/fond/create/", methods=["POST", "GET"])
def company_create_fond():
    form = FormFondCreate()
    message, result = None, False
    if request.method == 'POST':
        message = create_target(current_user.email, {"name": form.name.data, "description": form.description.data, "required_amount": form.required_amount.data})
        if "success" in message:
            return redirect("/login")
        message = list(message.values())[-1]
    return my_render("fond-create.html", title="Создать фонд", form=form, message=message)


@application.route("/fond/edit/<int:id>", methods=["POST", "GET"])
def company_edit_fond(id):
    form = FormFondEdit()
    # необязательно
    return my_render("fond-create.html", title="Редактировать фонд", form=form)


@application.route("/fond/delete/<int:id>", methods=["POST", "GET"])
def company_delete_fond(id):
    form = FormFondDelete()
    message = ""
    if request.method == 'POST':
        message = delete_target(current_user.email, id)
        if "success" in message:
            return redirect("/login")
        message = list(message.values())[-1]
    return my_render("fond-delete.html", title="Создать фонд", form=form, message=message)


if __name__ == '__main__':
    application.run()
