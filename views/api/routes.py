from flask import Blueprint,  request
from views.api.models import Mapper
from db import get_db
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

@api.route("/<model>")
def r_geo(model):

    def per_public(record): 
        result = {}
        result["ID_BNE"] =  record.get("id")
        result["Fuentes"] =  record.get("")
        result["Nombre"] = record.get("t_100")
        result["Género"] = record.get("t_375")
        result["Mas cosas"] =  record.get("")
        return result
    
    def geo_public(record): 
        result = {}
        result["ID_BNE"] =  record.get("id")
        result["Nombre"] =  record.get("t_781")
        result["lat_lng"] = record.get("lat_lng")
        return result

    # model = models.get(model)
    args = request.args
    try:
        t,v = tuple(*args.items())
    except Exception as e:
        pass
    start = time.perf_counter()
    # a = model.query.filter_by(t_375="|aMasculino").all()
    # a = [record.public() for record in a[0:100]]
    con = sqlite3.connect("instance/bne.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    def create_query(args:dict) -> str:
        query = f"SELECT * FROM {model} WHERE "
        for k,v in args.items():
            query += f"t_{k} LIKE '%{v}%' AND "
        return f"{query[0:-5]};"
    query = create_query(args)
    res = cur.execute(query)
    result = res.fetchall()
    if model.find("per") >= 0:
        to_show = [per_public(record) for record in result[0:10]]
    else:
        to_show = [geo_public(record) for record in result[0:10]]
    to_show = result[0:10]

    finish = time.perf_counter()
    total_t = finish-start
    data = {"time": total_t, "length": len(result), "data": to_show}
    return data

@api.route("/entry/<model>")
def r_entry_data_2(model):
    start = time.perf_counter()
    con = get_db()
    cur = con.cursor()
    inserter = Mapper()
    with open(f"converter/{model}.json", encoding="utf-8") as file:
        data = json.load(file)
        columns = len(tuple(cur.execute(f"pragma table_info({model});")))
        query = f"insert or ignore into {model} values ({'?, '*columns})"
        query = query.replace(", )", ")")
        cur.executemany(query,map(lambda record: inserter.extract_values(model, record), data))
        con.commit()
    finish = time.perf_counter()
    res = {"success": True, "time": finish-start}
    return res

@api.route("/test")
def r_test():
    db = get_db()
    return "TEST"
