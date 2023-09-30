from flask import Flask, render_template

application = Flask(__name__)


@application.route("/")
def main_page():
    return render_template("base.html")


@application.route("/log/")
def log_page():
    return render_template("log-form.html")


@application.route("/ui1/<int:coast>")
def ui_page(coast):
    if coast == 2:
        coast = -1
    return render_template("UI-kit.html", coast_motion=int(coast))


if __name__ == '__main__':
    application.run("192.168.1.109")