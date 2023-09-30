from flask import Flask, render_template

application = Flask(__name__)


@application.route("/")
def main_page():
    return render_template("base.html")


@application.route("/log/")
def log_page():
    return render_template("log-form.html")


if __name__ == '__main__':
    application.run("192.168.1.109")