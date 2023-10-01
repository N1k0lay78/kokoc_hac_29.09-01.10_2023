from flask import Flask, render_template, redirect, request

import config
from data import db_session
from data.forms import FormLogin, FormUserRegistration, FormCompanyRegistration

application = Flask(__name__)
# db_session.global_init("db/kokos.sqlite")
application.config.from_object(config)


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
    form = FormLogin()
    if request.method == "POST":
        # TODO:
        # session = db_session.create_session()
        # user = session.query(User).filter(User.email == form.email.data).first()
        # session.close()
        # if user and user.check_password(form.password.data):
        #     login_user(user, remember=True)
        return redirect("/")
    return my_render("login.html", title="Авторизация", need_log=False, form=form)


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


@application.route("/company/registration/<string:code>/", methods=["GET", "POST"])
def company_registration_page(code):
    form = FormCompanyRegistration()
    message, result = None, False
    # if request.method == 'POST':
    #     message = create_personaldata(current_user.email,  {"data": form.data.data, "typedata": form.typedata.data})
    #     if "success" in message:
    #         result = True
    #         set_special_params()
    #         return redirect('/admin')
    #     message = list(message.values())[-1]
    #     return redirect(f"/login")
    return my_render('company-registration.html', title="Регистрация", message=message, form=form, result=result)


@application.route("/log/")
def log_page():
    return my_render("log-form.html", need_log=False)


@application.route("/ui1/<int:coast>")
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
    application.run("192.168.1.109")