from flask import g
import sqlite3
from uuid import uuid4
from os import getcwd

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("query_saver.db")
    return db


def enter(query:str, length:int, date:str,ip:str,dataset:str,time:float):
    db = get_db()
    
    cur = db.cursor()
    
    query_str = f'''
                INSERT INTO queries VALUES(
                '{uuid4().hex}',
                "{query}",
                {length},
                '{date}',
                '{ip}',
                '{dataset}',
                {time}
                )
                '''
    print(query_str)
    cur.execute(query_str)
    db.commit()