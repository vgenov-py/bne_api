from flask import Blueprint,  request, render_template
from db import QMO

api = Blueprint("api", __name__)
'''

sqlite3 instance/bne.db .dump > back.sql
sqlite3 instance/bne.db < back.sql
mysqldump -u root xray --no-create-info > back_info.sql
mysqldump -u vgenovpy -h vgenovpy.mysql.eu.pythonanywhere-services.com --set-gtid-purged=OFF --no-tablespaces 'vgenovpy$xray'  > backup.sql
mysql -u vgenovpy -h vgenovpy.mysql.eu.pythonanywhere-services.com 'vgenovpy$xray'  < back.sql
mysql -u root -p xray < back.sql
'''


# @api.route("/")
# def r_home():
#     return render_template("index.html")

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

@api.route("/test")
def r_test():
    test_QMO = QMO("per", request.args)
    result = {}
    for t in test_QMO.available_fields:
        if t.startswith("t_"):
            a = test_QMO.cur.execute(f"SELECT count(id) as {t} FROM per  WHERE {t} is NULL and t_670 is not NULL;")
            result[t] = tuple(a)[0][t]
    # print(result)
    return "test_QMO.available_fields"



