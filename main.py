from flask import Flask, render_template

application = Flask(__name__)


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


@application.route("/ui1/<int:coast>")
def ui2_page(coast):
    if coast == 2:
        coast = -1
    return render_template("UI-kit-coast.html", coast_motion=int(coast))


@application.route("/ui2/")
def ui_page():
    return render_template("UI-kit-chart.html")


if __name__ == '__main__':
    application.run()