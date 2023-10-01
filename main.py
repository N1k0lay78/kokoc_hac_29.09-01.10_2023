import os
import random

import jsonpickle
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
import config
from data import db_session
from data.InnerAPI.InnerCompany import create_company
from data.InnerAPI.InnerTarget import create_target, delete_target
from data.InnerAPI.InnerUser import create_user
from data.InnerAPI.InnerUser import get_activity_statistics
from data.activity import Activity
from data.admin import Admin
from data.company import Company
from data.forms import FormLogin, FormUserRegistration, FormCompanyRegistration, FormFondEdit, FormFondCreate, \
    FormFondDelete, FormFondAdd, FormFondRemove
from data.user import User

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
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        user = session.query(Company).get(user_id)
        if not user:
            user = session.query(Admin).get(user_id)
            if not user:
                logout_user()
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
        session.close()
        if person and person.check_password(form.password.data):
            login_user(person, remember=True)
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
    print(data, email)
    return jsonpickle.encode(data)


@application.route("/user/profile/<int:id>/")
def user_profil_page(id):
    coast = 63_152.62  # in rub
    delta = 6.9  # %
    chart_types = ["анжумания", "анжумания", "анжумания", ]
    charts = [
        {
            "title": "анжумания",
            "subtitle": "за 1 раз 1000 rub",
            "avg_company": 10,
            "avg_user": 8,
            "data": [8,9,9,7,8,7,9]
        }, {
            "title": "анжумания",
            "subtitle": "за 1 раз 1000 rub",
            "avg_company": 10,
            "avg_user": 8,
            "data": [8,9,9,7,8,7,9]
        }, {
            "title": "анжумания",
            "subtitle": "за 1 раз 1000 rub",
            "avg_company": 10,
            "avg_user": 8,
            "data": [8,9,9,7,8,7,9]
        }   
    ]
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
    user_fonds = [
        [1, "Фонд №1", "Длинное описание фонда №1, очень длинное описание фонда, очеееень длинное", 56262.36, 42.54, True],
        [2, "Фонд №2", "Длинное описание фонда №2, очень длинное описание фонда, очеееень длинное", 94262.36, 78.12,  True],
        [3, "Фонд №3", "Длинное описание фонда №3, очень длинное описание фонда, очеееень длинное", 62262.36, 54.53,  False],

    ]
    return my_render("user-profile.html", is_authorized=True, is_logout=True, coast=coast,
                     increment=delta, leaderboard=leaderboard, chart_types=chart_types,
                     user_email=("" if current_user.is_anonymous else current_user.email), user_fonds=user_fonds)


@application.route("/user/work/")
def user_work():
    session = db_session.create_session()
    acts = session.query(Activity).all()
    types = set()
    for act in acts:
        types.add(act.type)
    types = list(types)
    print(types)
    print(acts)
    return my_render("user-work.html", types=types, acts=acts)



@application.route("/user/fonds/")
def user_fonds():
    # TODO:
    user_fonds = [
        [1, "Фонд №1", "Длинное описание фонда №1, очень длинное описание фонда, очеееень длинное", 56262.36, 42.54, True],
        [2, "Фонд №2", "Длинное описание фонда №2, очень длинное описание фонда, очеееень длинное", 94262.36, 78.12,  True],
        [3, "Фонд №3", "Длинное описание фонда №3, очень длинное описание фонда, очеееень длинное", 62262.36, 54.53,  False],
    ]
    return my_render("user-fonds.html", user_fonds=user_fonds)


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
def company_profile_page(id):
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

    fonds = [
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
    return my_render("company-profile.html", title="Профиль", is_logout=True, is_authorized=True,
                     leaderboard=leaderboard, fonds=fonds)


@application.route("/company/edit/", methods=["POST", "GET"])
def company_edit():
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
    if request.method == 'POST':
        message = delete_target(current_user.email, id)
        if "success" in message:
            return redirect("/login")
        message = list(message.values())[-1]
    return my_render("fond-delete.html", title="Создать фонд", form=form, message=message)


if __name__ == '__main__':
    application.run()
