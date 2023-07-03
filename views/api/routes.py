from flask import Blueprint,  request, render_template, make_response, Response, send_file
from db import QMO
import sqlite3
import time
import datetime as dt
import cProfile
import pstats
import msgspec
import csv
import orjson as json
from views.api.utils import enter 
import os
from qargs import Qargs
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
    args = {}
    for k,arg in request.args.items():
        args[k] = arg.replace(".csv", "")
    s = time.perf_counter()
    # with cProfile.Profile() as pr: # http://localhost:3000/api/per?t_375=masculino&limit=1000000
    print(dt.datetime.now())
    test_QMO = QMO(model, args)
    print("QMO: ",dt.datetime.now())
    data = test_QMO.query()
    

    if data["success"]:
        data["length"] = 0

        data["data"] = tuple(data["data"])
        print("data - TUPLE: ",dt.datetime.now())
        data["time"] = time.perf_counter() - s
        data["length"] += len(data["data"])
        print("TIME: ",data["time"])
        print(data["length"])
        now = dt.datetime.now()
        if request.url.find("csv") >= 0:
            os.system("rm -r download/*.csv")
            file_name = f"{now.year}{now.month}{now.day}{model}.csv"
            test_QMO.write_csv(file_name,data["data"])
            return send_file(f"{os.getcwd()}/download/{file_name}", as_attachment=True)
        enter(data["query"], data["length"], now, request.environ['REMOTE_ADDR'], model, data["time"])
    data = msgspec.json.encode(data)
    res = Response(response=data, mimetype="application/json", status=200)
    return res

@api.route("/fields/<model>")
def r_fields(model):
    res = {}
    test_QMO = QMO(model)
    view = request.args.get("view")
    if view:
        if view == "human":
            res["fields"] = []
            fields = test_QMO.human_fields
            for f in fields.split(","):
                if f.find("NULL") == -1:
                    res["fields"].append(f.split(".")[1])
        elif view == "marc":
            res["fields"] = []
            fields = test_QMO.marc_fields
            for f in fields.split(","):
                if f.find("NULL") == -1:
                    res["fields"].append(f.split(".")[1])

        return res
    res["fields"] = test_QMO.available_fields
    return res


@api.route("/entry/<model>")
def r_entry_data_2(model):
    test_QMO = QMO(model, f"converter/{model}.json")
    return test_QMO.insert()

@api.route("/blunt/<model>")
def r_blunt_query(model):
    res = QMO(model, request.args)
    with cProfile.Profile() as pr: # http://localhost:3000/api/per?t_375=masculino&limit=1000000

        data = res.blunt_query()
        if data["success"]:
            data["data"] = tuple(data["data"])
        data = json.dumps(data)
        # data = msgspec.json.encode(data)
        res = Response(response=data, mimetype="application/json", status=200)
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    return res


@api.route("/test")
def r_test():
    test_qmo = QMO("per")
    data = test_qmo.searches()
    data = tuple(data["data"])
    data = msgspec.json.encode(data)
    res = Response(response=data, mimetype="application/json", status=200)
    return res

@api.route("/qargs")
def r_qargs():
    data_purgue = QMO("per")
    print(data_purgue.purgue)
    test_1 = Qargs()
    return "test_1.query"



