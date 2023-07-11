from flask import Blueprint,  request, render_template, Response, send_file
from db import QMO
from mmo import MMO
import time
import datetime as dt
import cProfile
import pstats
import msgspec
import csv
import orjson as json
import os
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
            return render_template("csv.html", dataset=model)
        try:
            test_QMO.enter(data["query"], data["length"], now, request.environ['REMOTE_ADDR'], model, data["time"])
        except:
            pass
        data.pop("query")
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
    test_QMO = MMO(model)
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

@api.route("/searchesD2z2UAdAydEX1")
def r_searches():
    test_qmo = QMO("queries")
    data = test_qmo.searches()
    data = {"data":tuple(data["data"])}
    data["length"] = len(data["data"])
    data = msgspec.json.encode(data)
    res = Response(response=data, mimetype="application/json", status=200)
    return res

@api.route("/errorsD2z2UAdAydEX2")
def t_errors():
    with open("/var/log/bne_api/bne_api.err.log") as file:
        data = file.readlines()
        return render_template("errors_log.html",data=data)
    
@api.route("/schema")
def t_schema():
    return render_template("schema.html")

@api.route("/stats")
def t_stats():
    test_qmo = QMO("queries")
    data = test_qmo.searches()
    data = tuple(data["data"])
    # data = msgspec.json.encode(data)
    # res = Response(response=data, mimetype="application/json", status=200)
    return render_template("stats.html")




