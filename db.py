# from flask_sqlalchemy import SQLAlchemy
from constants import DB_FILE
# db = SQLAlchemy()

import sqlite3
from flask import g

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    return db

