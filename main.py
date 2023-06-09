from flask import Flask, g
import os
from views.api.routes import api
from views.home.routes import web
from views.errors.routes import errors
from constants import SECRET_KEY, DB_FILE
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["TIMEZONE"] = "Europe/Madrid"
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSON_AS_ASCII'] = False
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(errors)
    app.register_blueprint(web)
    return app

def set_db():
    os.system("mkdir instance")
    os.system("sqlite3 instance/bne.db < .schema.sql")

app = create_app()
CORS(app)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if "kuga" in app.root_path:
    if __name__ == "__main__":
        if not os.path.isfile(DB_FILE):
            set_db()
        app.run(debug=True, port=3000)
else:
    app = create_app()
    if not os.path.isfile(DB_FILE):
        set_db()
