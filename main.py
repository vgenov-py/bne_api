from flask import Flask
from db import db
import os
from views.api.routes import api
from constants import SECRET_KEY, DB_FILE, DATABASE_URI


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["TIMEZONE"] = "Europe/Madrid"
    app.config['JSON_SORT_KEYS'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE}"
    # app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.register_blueprint(api, url_prefix="/api")
    db.init_app(app)
    return app

def set_db(app):
    with app.app_context():
        db.create_all()

app = create_app()
if "kuga" in app.root_path:
    if __name__ == "__main__":
        if not os.path.isfile(DB_FILE):
            set_db(app)
        app.run(debug=True, port=3000)
else:
    app = create_app()
    if not os.path.isfile(DB_FILE):
        set_db(app)
