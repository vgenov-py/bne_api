from flask import Blueprint,  request, render_template
from views.api.models import Mapper
from db import get_db, QMO
import time
import sqlite3
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

api = Blueprint("api", __name__)
'''

sqlite3 instance/bne.db .dump > back.sql
sqlite3 instance/bne.db < back.sql
mysqldump -u root xray --no-create-info > back_info.sql
mysqldump -u vgenovpy -h vgenovpy.mysql.eu.pythonanywhere-services.com --set-gtid-purged=OFF --no-tablespaces 'vgenovpy$xray'  > backup.sql
mysql -u vgenovpy -h vgenovpy.mysql.eu.pythonanywhere-services.com 'vgenovpy$xray'  < back.sql
mysql -u root -p xray < back.sql
'''

# models = {"per":Per, "geo": Geo}

@api.route("/")
def r_home():
    return render_template("index.html")

@api.route("/<model>")
def r_dataset(model):
    limit = request.args.get("limit")
    limit = limit if limit else 1000
    args = request.args
    try:
        t,v = tuple(*args.items())
    except Exception as e:
        pass
    start = time.perf_counter()
    cur = get_db().cursor()
    def create_query(args:dict) -> str:
        fields = request.args.get("fields")
        if fields:
            query = f"SELECT {fields} FROM {model} WHERE "
        else:
            query = f"SELECT * FROM {model} WHERE "

        for k,v in args.items():
            if k in ["limit", "fields"]:
                continue
            if k.isdigit():
                query += f"t_{k} LIKE '%{v}%' AND "
            else:
                query += f"{k} LIKE '%{v}%' AND "

        return f"{query[0:-5]};"
    query = create_query(args)
    res = cur.execute(query)
    def get_results_limit(data, limit: int):
        limit = int(limit)
        counter = 0
        for record in data:
            if counter < limit:
                yield record
            else:
                return
            counter += 1
    finish = time.perf_counter()
    result = list(get_results_limit(res, limit))
    total_t = finish-start
    data =  {"success":True, "time": total_t, "length": len(result), "data": result}
    return data

@api.route("/entry/<model>")
def r_entry_data_2(model):
    test_QMO = QMO(model, f"converter/{model}.json")
    return test_QMO.insert()

@api.route("/test")
def r_test():
    test_QMO = QMO("per", request.args)
    return test_QMO.query()
