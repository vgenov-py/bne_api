from flask import Blueprint,  request, render_template
from db import QMO
import sqlite3
import time
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

@api.route("/<model>")
def r_query(model):
    test_QMO = QMO(model, request.args)
    return test_QMO.query()

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
    con = sqlite3.connect("instance/bne.db")
    con = sqlite3.connect(":memory:")
    con.row_factory = dict_factory
    cur = con.cursor()
    res = cur.execute("SELECT id FROM per where t_375 like '%masculino%' LIMIT 100")
    return {"time":time.perf_counter()-start, "data": list(res)}



