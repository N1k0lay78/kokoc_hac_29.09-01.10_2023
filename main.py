from flask import Flask, render_template
from data import db_session

application = Flask(__name__)
db_session.global_init("db/kokos.sqlite")


@application.route("/")
def main_page():
    return render_template("base.html")


@application.route("/log/")
def log_page():
    return render_template("log-form.html")


if __name__ == '__main__':
    application.run()