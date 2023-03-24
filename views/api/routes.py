from flask import Blueprint,  request
from views.api.models import  Geo, Per
from db import db
from sqlalchemy import text
import time
import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

api = Blueprint("api", __name__)
'''
sqlite3 instance/xray.db .dump > back.sql
sqlite3 instance/xray.db < back.sql
mysqldump -u root xray --no-create-info > back_info.sql
mysqldump -u vgenovpy -h vgenovpy.mysql.eu.pythonanywhere-services.com --set-gtid-purged=OFF --no-tablespaces 'vgenovpy$xray'  > backup.sql
mysql -u vgenovpy -h vgenovpy.mysql.eu.pythonanywhere-services.com 'vgenovpy$xray'  < back.sql
mysql -u root -p xray < back.sql
'''

models = {"per":Per, "geo": Geo}

@api.route("/<model>")
def r_geo(model):

    def public(record): 
        result = {}
        result["ID_BNE"] =  record.get("id")
        result["Fuentes"] =  record.get("")
        result["Nombre"] = record.get("t_100")
        result["Género"] = record.get("t_375")
        result["Mas cosas"] =  record.get("")
        return result

    model = models.get(model)
    args = request.args
    try:
        t,v = tuple(*args.items())
    except Exception as e:
        pass
    # with open("converter/persona1.json", encoding="utf-8") as file:
    #     data = json.load(file)
    #     # def gen_record(record):
    #     #     record["001"] = record.get("001")[2:]
    #     #     try:
    #     #         yield model(record)
    #     #     except Exception as e:
    #     #         e
    #     for record in data[70000:]:
    #         record["001"] = record.get("001")[2:]
    #         # query= f'''
    #         #     INSERT OR IGNORE INTO person (id, t_003, t_005, t_008, t_024, t_046, t_100, t_368, t_370, t_372, t_373, t_374, t_375, t_377, t_400, t_500, t_670) VALUES {tuple(record.values())};
    #         # '''
    #         try:
    #             record = model(record)
    #             db.session.add(record)
    #         except Exception as e:
    #             print(e)
    #         try:
    #             db.session.commit()
    #         except Exception as e:
    #             print(e)
        # db.session.bulk_save_objects(map(lambda record: gen_record(record),data))
    start = time.perf_counter()
    # a = model.query.filter_by(t_375="|aMasculino").all()
    # a = [record.public() for record in a[0:100]]
    con = sqlite3.connect("instance/bne.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    # res = cur.execute(f'''SELECT * FROM person where t_{t} = "{v}"''')
    # res = cur.execute(f'''SELECT * FROM person where instr(t_{t}, '{v}') > 0''')
    def create_query(args:dict) -> str:
        query = "SELECT * FROM person WHERE "
        for k,v in args.items():
            query += f"t_{k} LIKE '%{v}%' AND "
        return f"{query[0:-5]};"
    query = create_query(args)
    print(query)
    res = cur.execute(query)
    result = res.fetchall()
    to_show = [public(record) for record in result[0:10]]
    finish = time.perf_counter()
    total_t = finish-start
    data = {"time": total_t, "length": len(result), "data": to_show}
    return data