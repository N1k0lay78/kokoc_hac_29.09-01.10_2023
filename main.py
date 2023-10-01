from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, logout_user, login_required, login_user, current_user

import config
from data import db_session
from data.InnerAPI.InnerCompany import create_company
from data.admin import Admin
from data.company import Company
from data.forms import FormLogin, FormUserRegistration, FormCompanyRegistration
from data.user import User

application = Flask(__name__)
# db_session.global_init("db/kokos.sqlite")
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
        "is_authorized": False,  # need irl data
        "is_logout": False,
        "user_id": -1,  # need irl data
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
            return redirect("/") # если успех
        return redirect("/") # если неуспех
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


@application.route("/company/registration", methods=["GET", "POST"])
def company_registration_page():
    form = FormCompanyRegistration()
    message, result = None, False
    if request.method == 'POST':
        if form.password_1.data == form.password_2.data:
            message = create_company({"name": form.name.data, "email": form.email.data, "rates": form.rates.data, "logo": "./static/img/kokoc_logo.png", "password": form.password_1.data})
            if "success" in message:
                return redirect("/login")
            message = list(message.values())[-1]
        else:
            message = "Пароли не совпадают"
        return redirect(f"/login")
    return my_render('company-registration.html', title="Регистрация", message=message, form=form, result=result)


@application.route("/company/<string:name>/")
def company_page(name):
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
    return my_render("company-profile.html", title="Профиль", is_logout=True, is_authorized=True, leaderboard=leaderboard, fonds=fonds)


@application.route("/fond/create/", methods=["POST", "GET"])
def company_create_fond():
    return redirect("/company/profile/123")


@application.route("/fond/edit/<int:id>", methods=["POST", "GET"])
def company_edit_fond():
    return redirect("/company/profile/123")


@application.route("/fond/delete/<int:id>", methods=["POST", "GET"])
def company_delete_fond():
    return redirect("/company/profile/123")


@application.route("/company/edit/", methods=["POST", "GET"])
def company_edit():
    return redirect("/company/profile/123")


@application.route("/log/")
def log_page():
    return my_render("log-form.html", need_log=False)


@application.route("/ui1/<int:coast>/")
def ui1_page(coast):
    if coast == 2:
        coast = -1
    return my_render("UI-kit-coast.html", coast_motion=int(coast))


@application.route("/ui2/")
def ui2_page():
    return my_render("UI-kit-chart.html")


@application.route("/ui3/<int:id>")
def ui3_page(id):
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
    return my_render("UI-kit-leaderboard.html", leaderboard=leaderboard, user_id=id, need_log=True)


if __name__ == '__main__':
    application.run()