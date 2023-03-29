from constants import DB_FILE
import sqlite3
from flask import g
import re
import json
import time

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_FILE)
    db.row_factory = dict_factory
    return db

class QMO:
    def __init__(self,dataset:str,  args:dict=None, json_file:str=None):
        self.dataset = dataset
        self.args = args
        self.json_file = json_file

    @property
    def time(self):
        return time.perf_counter()
    
    @property
    def con(self):
        return get_db()
    
    @property
    def cur(self):
        return self.con.cursor()
    
    @property
    def available_fields(self) -> tuple:
        res = tuple(map(lambda column: column["name"], self.cur.execute(f"pragma table_info({self.dataset});")))
        return res
    
    @property
    def splitter(self):
        return " /**/ "
    
    @property
    def res_json(self):
        res = {"success":False}
        return res

    def extract_values(self,dataset:str ,record:dict) -> tuple:
        result = []
        if dataset == "geo":
            result.append(record.get("001")[2:])
            result.append(record.get("001"))
            result.append(record.get("024"))
            result.append(record.get("034"))
            result.append(record.get("080"))
            result.append(record.get("151"))
            result.append(record.get("451"))
            result.append(record.get("510"))
            result.append(record.get("550"))
            result.append(record.get("551"))
            result.append(record.get("667"))
            result.append(record.get("670"))
            result.append(record.get("781"))
            humans = []
            humans.append(self.dollar_parser(record.get("001"))  if record.get("001") else None)
            humans.append(self.other_identifiers(record.get("024"))  if record.get("024") else None)
            humans.append(self.f_lat_lng(record.get("034")) if self.f_lat_lng(record.get("034")) else None)
            #CDU:
            humans.append(self.dollar_parser(record.get("080")) if record.get("080") else None)
            #nombre de lugar:
            humans.append(self.dollar_parser(record.get("151"))  if record.get("151") else None)
            #otros nombres de lugar
            humans.append(self.dollar_parser(record.get("451"))  if record.get("451") else None)
            #entidad relacionada
            humans.append(self.dollar_parser(record.get("510"))  if record.get("510") else None)
            #materia relacionada
            humans.append(self.dollar_parser(record.get("550"))  if record.get("550") else None)
            #lugar relacionado
            humans.append(self.related_place(record.get("551"))  if record.get("551") else None)
            #nota general
            humans.append(self.dollar_parser(record.get("667"))  if record.get("667") else None)
            #fuentes de información
            humans.append(self.sources(record.get("670"))  if record.get("670") else None)
            #lugar jerárquico
            humans.append(self.dollar_parser(record.get("781")) if record.get("781") else None)
            #obras relacionadas en el catálogo BNE
            humans.append(self.gen_url(record.get("001"))  if record.get("001") else None)
            result.extend(humans)

        elif dataset == "per":
            result.append(record.get("001")[2:])
            result.append(record.get("001"))
            result.append(record.get("003"))
            result.append(record.get("005"))
            result.append(record.get("008"))
            result.append(record.get("024"))
            result.append(record.get("046"))
            result.append(record.get("100"))
            result.append(record.get("368"))
            result.append(record.get("370"))
            result.append(record.get("372"))
            result.append(record.get("373"))
            result.append(record.get("374"))
            result.append(record.get("375"))
            result.append(record.get("400"))
            result.append(record.get("377"))
            result.append(record.get("500"))
            result.append(record.get("670"))

        elif dataset == "mon":
            result.append(record.get("001")[2:] if record.get("001") else uuid4().hex)
            result.append(record.get("001"))
            result.append(record.get("035"))
            result.append(record.get("040"))
            result.append(record.get("100"))
            result.append(record.get("130"))
            result.append(record.get("245"))
            result.append(record.get("260"))
            result.append(record.get("300"))
            result.append(record.get("500"))
            result.append(record.get("899"))
            result.append(record.get("927"))
            result.append(record.get("980"))
            result.append(record.get("994"))
            
        return tuple(result)
    
    def dollar_parser(self, value: str) -> str:
        re_dollar = "\|\w{1}"
        result = re.sub(re_dollar, "", value, 1)
        result = re.sub(re_dollar, ", ", result)
        return result
    
    def other_identifiers(self, value:str) -> str:
        result = ""
        value_splitted = value.split(self.splitter)
        for v_s in value_splitted:
            try:
                _, url, source = re.split("\|\w{1}", v_s)
                result += f"{source}: {url}{self.splitter}"
            except Exception:
                    pass
        return result
    
    def related_place(self, value:str) -> str:
        result = ""
        value_splitted = value.split(self.splitter)
        for v_s in value_splitted:
            try:
                _, place = re.split("\|a", v_s, 1)
                result += f"{place}{self.splitter}"
            except Exception:
                pass
    
    def sources(self, value: str) -> str:
        result = ""
        value_splitted = value.split(self.splitter)
        for v_s in value_splitted:
            try:
                _, source, place = re.split("\|\w{1}", v_s)
                result += f"{source}: {place}{self.splitter}"
            except:
                pass
        return result

    def gen_url(self, value: str) -> str:
        result = "http://catalogo.bne.es/uhtbin/cgisirsi/0/x/0/05?searchdata1="
        result += value[4:]
        return result          

    def f_lat_lng(self, v):
        re_coord = "\w{2}\d{1,}"
        result = ""
        try:
            a = re.findall(re_coord, v)
            for i, coord in enumerate(a):
                if i % 2 == 0:
                    coord = coord[1:]
                    c_point = coord[0]
                    digits = coord[1:]
                    n = float(f"{digits[0:3]}.{digits[3:]}")
                    if c_point == "W" or c_point == "E":
                        if c_point == "W":
                            n = -n
                        result += f"{n}"
                    else:
                        if c_point == "S":
                            n = -n
                        result += f", {n}"
        
            return result
        except:
            return None

    @property
    def purgue(self):
        res_json = self.res_json
        args = self.args.copy()
        fields = args.pop("fields", None)
        limit = args.pop("limit", "1000")
        if limit:
            try:
                 int(limit)
            except ValueError as e:
                res_json["message"] = f"Limit value should be an integer"
                return res_json
        res_json["limit"] = limit  
        for field in fields.split(",") if fields else ():
            field:str = field.strip()
            if field not in self.available_fields:
                res_json["message"] = f"This field doesn't exist in the db: {field} - available fields: {self.available_fields}"
                # res_json["available_fields"] = f"{self.available_fields}"
                return res_json
        res_json["fields"] = fields
        
        not_available_field = next(filter(lambda kv: kv[0] not in self.available_fields, args.items()), None)
        if not_available_field:
            res_json["message"] = f"This field doesn't exist in the db: {not_available_field[0]}  - available fields: {self.available_fields}"
            return res_json
        res_json["args"] = args
        res_json["success"] = True
        return res_json
    
    def query(self):
        start = self.time
        res_json = self.purgue
        print(res_json)
        if not res_json["success"]:
            return {"success":False,"message":res_json["message"]}
        fields = res_json['fields'] if res_json['fields'] else '*'
        # query = f"SELECT {fields} FROM {self.dataset}  LIMIT {res_json['limit']};"
        query = f"SELECT {fields} FROM {self.dataset} WHERE "
        for k,v in res_json["args"].items():
            if v == "null":
                query += f"{k} is NULL AND "
            else:
                query += f"{k} LIKE '%{v}%' AND "
        
        query = f"{query[0:-5]} LIMIT {res_json['limit']};"
        print(query)
        res = list(self.cur.execute(query))
        res_json = self.res_json
        res_json["success"] = True
        res_json["length"] = len(res)
        res_json["time"] = self.time - start
        res_json["data"] = res
        return res_json
    
    def insert(self):
        res_json = {"success":False}
        with open(f"converter/{self.dataset}.json", encoding="utf-8") as file:
            try:
                data = json.load(file)
                query = f"insert or ignore into {self.dataset} values ({'?, '*len(self.available_fields)})"
                query = query.replace(", )", ")")
                self.cur.executemany(query,map(lambda record: self.extract_values(self.dataset, record), data))
                self.con.commit()
                res_json["success"] = True
                return res_json
            except Exception as e:
                res_json["message"] = f"{e}"
                return res_json