from flask import Blueprint,  request, render_template, make_response, Response
from db import QMO
import sqlite3
import time
import orjson as json
import cProfile
import pstats
api = Blueprint("api", __name__)
'''

sqlite3 instance/bne.db .dump > back.sql
sqlite3 instance/bne.db < back.sql
mysqldump -u root xray --no-create-info > back_info.sql
mysqldump -u vgenovpy -h vgenovpy.mysql.eu.pythonanywhere-services.com --set-gtid-purged=OFF --no-tablespaces 'vgenovpy$xray'  > backup.sql
mysql -u vgenovpy -h vgenovpy.mysql.eu.pythonanywhere-services.com 'vgenovpy$xray'  < back.sql
mysql -u root -p xray < back.sql
'''


@api.route("/")
def r_home():
    test = QMO("per")
    return render_template("index.html")

# @api.route("/<model>")
# def r_query(model):
#     test_QMO = QMO(model, request.args)
#     return test_QMO.query()

@api.route("/<model>")
def r_query(model):
    s = time.perf_counter()
    test_QMO = QMO(model, request.args)
    with cProfile.Profile() as pr: # http://localhost:3000/api/per?t_375=masculino&limit=1000000
        data = test_QMO.query()
        # e = time.perf_counter()
        # print("DB ",e-s, " DB")
        # s = time.perf_counter()
        # data = json.dumps(data)
        data["data"] = tuple(map(lambda row:dict(zip(data["av"],row)),data["data"]))
        data = json.dumps(data)
        res = Response(response=data, mimetype="application/json", status=200)
        # e = time.perf_counter()
        # print("JSON ",e-s, " JSON")
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    return res

@api.route("/entry/<model>")
def r_entry_data_2(model):
    test_QMO = QMO(model, f"converter/{model}.json")
    return test_QMO.insert()

@api.route("/blunt")
def r_blunt_query():
    res = QMO("", request.args)
    return res.blunt_query()

# @api.route("/test")
# def r_test():
#     test_QMO = QMO("per", request.args)
#     result = {}
#     for t in test_QMO.available_fields:
#         if t.startswith("t_"):
#             a = test_QMO.cur.execute(f"SELECT count(id) as {t} FROM per  WHERE {t} is NULL and t_670 is not NULL;")
#             result[t] = tuple(a)[0][t]
#     # print(result)
#     return "test_QMO.available_fields"

@api.route("/test")
def r_test():
    start = time.perf_counter()
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    con = sqlite3.connect("instance/bne.db", isolation_level=None)
    con.row_factory = dict_factory
    # cur = con.cursor()
    con.execute("PRAGMA journal_mode=wal")
    data = list(con.execute("SELECT * FROM per where t_375 like '%masculino%'"))
    delta = time.perf_counter()-start
    res = {
        "time":delta,
        "data":data
    }
    res = make_response(json.dumps(data).encode("utf8"))
    res.headers["mime-type"] = "application/json"
    print(delta)
    print(time.perf_counter() - start )
    return res



