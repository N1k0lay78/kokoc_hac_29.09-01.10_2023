from flask import Flask, render_template
from data import db_session

application = Flask(__name__)
# db_session.global_init("db/kokos.sqlite")


@application.route("/")
def main_page():
    return render_template("base.html")


@application.route("/log/")
def log_page():
    return render_template("log-form.html")


@application.route("/ui1/<int:coast>")
def ui1_page(coast):
    if coast == 2:
        coast = -1
    return render_template("UI-kit-coast.html", coast_motion=int(coast))


@application.route("/ui2/")
def ui2_page():
    return render_template("UI-kit-chart.html")


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
    return render_template("UI-kit-leaderboard.html", leaderboard=leaderboard, user_id=id)


if __name__ == '__main__':
    application.run("192.168.1.109")