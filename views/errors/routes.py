from flask import Blueprint, render_template, request
errors = Blueprint("errors", __name__)
import datetime as dt

def write_error(error):
    with open("logs/errors.log", "a", encoding="utf-8") as file:
        file.write(f"{dt.datetime.now()} | {error} | {request.url}\n")

@errors.app_errorhandler(404)
def error_404(error):
    write_error(error)
    return render_template("errors/404.html"), 404

@errors.app_errorhandler(403)
def error_403(error):
    write_error(error)
    return render_template("errors/404.html"), 403

@errors.app_errorhandler(500)
def error_500(error):
    write_error(error)
    return render_template("errors/404.html"), 500
