from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, logout_user, login_required, login_user, current_user

import config
from data import db_session
from data.InnerAPI.InnerCompany import create_company
from data.admin import Admin
from data.company import Company
from data.forms import FormLogin, FormUserRegistration, FormCompanyRegistration, FormFondEdit, FormFondCreate, \
    FormFondDelete
from data.user import User

application = Flask(__name__)
db_session.global_init("db/kokos.sqlite")
application.config.from_object(config)
login_manager = LoginManager()
login_manager.init_app(application)


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
def user_registration_page(code):
    form = FormUserRegistration()
    message, result = None, False
    # if request.method == 'POST':
    #     message = create_personaldata(current_user.email,  {"data": form.data.data, "typedata": form.typedata.data})
    #     if "success" in message:
    #         result = True
    #         set_special_params()
    #         return redirect('/admin')
    #     message = list(message.values())[-1]
    #     return redirect(f"/login")
    return my_render('user-registration.html', title="Регистрация", message=message, form=form, result=result)


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
    return my_render("user-profile.html", is_authorized=True, is_logout=True, coast=coast,
                     increment=delta, leaderboard=leaderboard, chart_types=chart_types)


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
        return redirect(f"/login")
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
    # TODO:
    # создание фонда
    return my_render("fond-create.html", title="Создать фонд", form=form)


@application.route("/fond/edit/<int:id>", methods=["POST", "GET"])
def company_edit_fond(id):
    form = FormFondEdit()
    # необязательно
    return my_render("fond-create.html", title="Редактировать фонд", form=form)


@application.route("/fond/delete/<int:id>", methods=["POST", "GET"])
def company_delete_fond(id):
    form = FormFondDelete()
    # TODO:
    # удаление фонда
    return my_render("fond-delete.html", title="Создать фонд", form=form)


if __name__ == '__main__':
    application.run()
