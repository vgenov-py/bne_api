from constants import DB_FILE
import sqlite3
from flask import g
import re
import time
from uuid import uuid4
import msgspec
from typing import Optional


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_FILE)
    # db.row_factory = dict_factory
    # db.row_factory = sqlite3.Row
    return db

class Per(msgspec.Struct, omit_defaults=True, gc=True):
    id: Optional[str] = None
    t_001: Optional[str] = None
    t_024: Optional[str] = None
    t_046: Optional[str] = None
    t_100: Optional[str] = None
    t_368: Optional[str] = None
    t_370: Optional[str] = None
    t_372: Optional[str] = None
    t_373: Optional[str] = None
    t_374: Optional[str] = None
    t_375: Optional[str] = None
    t_377: Optional[str] = None
    t_400: Optional[str] = None
    t_500: Optional[str] = None
    t_510: Optional[str] = None
    t_670: Optional[str] = None
    otros_identificadores: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    fecha_muerte: Optional[str] = None
    nombre_de_persona: Optional[str] = None
    otros_atributos_persona: Optional[str] = None
    lugar_nacimiento: Optional[str] = None
    lugar_muerte: Optional[str] = None
    pais_relacionado: Optional[str] = None
    otros_lugares_relacionados: Optional[str] = None
    lugar_residencia: Optional[str] = None
    campo_actividad: Optional[str] = None
    grupo_o_entidad_relacionada: Optional[str] = None
    ocupacion: Optional[str] = None
    genero: Optional[str] = None
    lengua: Optional[str] = None
    otros_nombres: Optional[str] = None
    persona_relacionada: Optional[str] = None
    fuentes_de_informacion: Optional[str] = None
    obras_relacionadas_en_el_catalogo_BNE: Optional[str] = None

class Geo(msgspec.Struct, omit_defaults=True):
    id:Optional[str] = None
    t_001:Optional[str] = None
    t_024:Optional[str] = None
    t_034:Optional[str] = None
    t_080:Optional[str] = None
    t_151:Optional[str] = None
    t_451:Optional[str] = None
    t_510:Optional[str] = None
    t_550:Optional[str] = None
    t_551:Optional[str] = None
    t_667:Optional[str] = None
    t_670:Optional[str] = None
    t_781:Optional[str] = None
    otros_identificadores:Optional[str] = None
    coordenadas_lat_lng:Optional[str] = None
    CDU:Optional[str] = None
    nombre_de_lugar:Optional[str] = None
    otros_nombres_de_lugar:Optional[str] = None
    entidad_relacionada:Optional[str] = None
    materia_relacionada:Optional[str] = None
    lugar_relacionado:Optional[str] = None
    nota_general:Optional[str] = None
    fuentes_de_informacion:Optional[str] = None
    lugar_jerarquico:Optional[str] = None
    obras_relacionadas_en_el_catalogo_BNE:Optional[str] = None

class Mon(msgspec.Struct, omit_defaults=True):
    id:Optional[str] = None
    t_001:Optional[str] = None
    t_008:Optional[str] = None
    t_020:Optional[str] = None
    t_035:Optional[str] = None
    t_040:Optional[str] = None
    t_100:Optional[str] = None
    t_130:Optional[str] = None
    t_245:Optional[str] = None
    t_260:Optional[str] = None
    t_300:Optional[str] = None
    t_500:Optional[str] = None
    t_700:Optional[str] = None
    t_899:Optional[str] = None
    t_927:Optional[str] = None
    t_980:Optional[str] = None
    t_994:Optional[str] = None
    per_id:Optional[str] = None

structs = {
    "geo": Geo,"per":Per, "mon":Mon
}


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
        # res = tuple(map(lambda column: column["name"], self.cur.execute(f"pragma table_info({self.dataset});")))
        return [row[1] for row in tuple(self.cur.execute(f"pragma table_info({self.dataset});"))]
        return res
    
    @property
    def virtual_fields(self) -> tuple:
        # res = tuple(map(lambda column: column["name"], self.cur.execute(f"pragma table_info({self.dataset}_fts);")))
        return [row[1] for row in tuple(self.cur.execute(f"pragma table_info({self.dataset}_fts);"))]

        return res
    
    @property
    def marc_fields(self) -> tuple:
        result = ""
        for field in self.cur.execute(f"pragma table_info({self.dataset});"):
            field:str = field[1]
            if field.startswith("t_"):
                result += f", {field}"
            else:
                result += f", NULL"
        return result[2:]

    
    @property
    def human_fields(self) -> tuple:
        result = ""
        for field in self.cur.execute(f"pragma table_info({self.dataset});"):
            field:str = field[1]
            if not field.startswith("t_"):
                result += f", {field}"
            else:
                result += f", NULL"
        return result[2:]
        
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
            # humans.append(self.dollar_parser(record.get("001"))  if record.get("001") else None)
            humans.append(self.other_identifiers(record.get("024")))
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
            result.append(record.get("024"))
            result.append(record.get("046"))
            result.append(record.get("100"))
            result.append(record.get("368"))
            result.append(record.get("370"))
            result.append(record.get("372"))
            result.append(record.get("373"))
            result.append(record.get("374"))
            result.append(record.get("375"))
            result.append(record.get("377"))
            result.append(record.get("400"))
            result.append(record.get("500"))
            result.append(record.get("510"))
            # result.append(record.get("667"))
            result.append(record.get("670"))
            # result.append(record.get("678"))
            #HUMANS:
            # result.append(self.get_single_dollar(record.get("001"),"a"))
            # otros_identificadores
            result.append(self.other_identifiers(record.get("024")))
            # fecha de nacimiento
            result.append(self.get_single_dollar(record.get("046"), "f"))
            # fecha de muerte
            result.append(self.get_single_dollar(record.get("046"), "g"))
            # nombre de persona
            result.append(self.per_person_name(record.get("100")))
            # otros atributos persona
            result.append(self.per_other_attributes(record.get("368")))
            #lugar de nacimiento
            result.append(self.get_single_dollar(record.get("370"), "a"))
            #lugar de muerte
            result.append(self.get_single_dollar(record.get("370"), "b"))
            #país relacionado
            result.append(self.get_single_dollar(record.get("370"), "c"))
            #otros lugares relacionados
            result.append(self.get_single_dollar(record.get("370"), "f"))
            #lugar residencia
            result.append(self.get_single_dollar(record.get("370"), "e"))
            #campo_actividad
            result.append(self.get_single_dollar(record.get("372"), "a"))
            #grupo o entidad relacionada
            result.append(self.group_or_entity(record))
            #ocupacion
            result.append(self.dollar_parser(record.get("374")))
            #género
            result.append(self.get_single_dollar(record.get("375"), "a"))
            #lengua
            result.append(self.get_single_dollar(record.get("377"), "l"))
            #otros nombres
            result.append(self.per_person_name(record.get("400")))
            #persona relacionada
            result.append(self.per_person_name(record.get("500")))
            #nota general
            # result.append(self.dollar_parser(record.get("667")))
            #fuentes de información
            result.append(self.per_other_sources(record.get("670")))
            #otros datos biográficos
            # result.append(self.dollar_parser(record.get("678")))
            #obras relacionadas en el catálogo BNE
            result.append(self.per_gen_url(record.get("001")))

        elif dataset == "mon":
            result.append(record.get("001")[2:] if record.get("001") else uuid4().hex)
            result.append(record.get("001"))
            result.append(record.get("008"))
            result.append(record.get("020"))
            result.append(record.get("035"))
            result.append(record.get("040"))
            result.append(record.get("100"))
            result.append(record.get("130"))
            result.append(record.get("245"))
            result.append(record.get("260"))
            result.append(record.get("300"))
            result.append(record.get("500"))
            result.append(record.get("700"))
            result.append(record.get("899"))
            result.append(record.get("927"))
            result.append(record.get("980"))
            result.append(record.get("994"))
            result.append(self.mon_per_id(record.get("100")))
            
        return tuple(result)
    
    def get_single_dollar(self, value:str, dollar: str) -> str:
        if not value:
            return None
        re_selected_dollar = f"\|{dollar}([ \S]*?)\||\|{dollar}([ \S+]+)"
        value = re.search(re_selected_dollar, value)
        if value:
             for match in value.groups():
                  if match:
                       return match
    
    def dollar_parser(self, value: str) -> str:
        if not value:
            return None
        re_dollar = "\|\w{1}"
        result = re.sub(re_dollar, "", value, 1)
        result = re.sub(re_dollar, ", ", result)
        return result
    
    def other_identifiers(self, value:str) -> str:
        if not value:
            return None
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
                # place = self.get_single_dollar(v_s, "a")
                result += f"{place}{self.splitter}"
            except Exception:
                pass
        return result
    
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

    def per_geo_id(self, v: str) -> str:
        '''
        This would get de geo id from the 370's
        '''
        if v: 
            result = re.findall("XX\d{4,7}", v)
            if len(result):
                return result[0]
        else:
            return        

    
    def per_person_name(self, value: str) -> str:
        if not value:
            return
        dollar_a = self.get_single_dollar(value, "a")
        result = f"{dollar_a}"
        dollar_b = self.get_single_dollar(value, "b")
        if dollar_b:
            result += f", {dollar_b}"
        dollar_c = self.get_single_dollar(value, "c")
        if dollar_c:
            result += f", {dollar_c}"
        dollar_d = self.get_single_dollar(value, "d")
        if dollar_d:
            result += f", ({dollar_d})" 
        dollar_q = self.get_single_dollar(value, "q")
        if dollar_q:
            result += f", ({dollar_q})"
        return result
    
    def per_other_attributes(self, value:str) -> str:
        if not value:
            return
        result = ""
        value_splitted = value.split(self.splitter)
        for v_s in value_splitted:
            try:
                if self.get_single_dollar(v_s, "c"):
                    result += self.get_single_dollar(v_s, "c") + self.splitter
                if self.get_single_dollar(v_s, "d"):
                    result += self.get_single_dollar(v_s, "d") + self.splitter
            except Exception:
                    pass
        return result[0:-6]
        
    def per_other_sources(self, value:str) -> str:
        if not value:
            return
        result = ""
        for v_s in value.split(self.splitter):
            dollar_a = self.get_single_dollar(v_s, "a")
            dollar_b = self.get_single_dollar(v_s, "b")
            dollar_u = self.get_single_dollar(v_s, "u")
            if dollar_a and dollar_b:
                if result:
                    result += f", {dollar_a}: {dollar_b}"
                else:
                    result = f"{dollar_a}: {dollar_b}"
                if dollar_u:
                    result += f" ({dollar_u})"
        return result
    
    def per_gen_url(self, value: str) -> str:
        if not value:
            return None
        result = "http://catalogo.bne.es/uhtbin/cgisirsi/0/x/0/05?searchdata1=%5ea"
        result += value[4:]
        return result   

    def group_or_entity(self, record:dict) -> str:
        t_373 = record.get("373")
        t_510 = record.get("510")
        if not t_373 and not t_510:
            return
        result = ""
        if t_373:
            t_373 = self.dollar_parser(t_373)
            for value in t_373.split("/**/"):
                result += value.split(", ")[0]
        if t_510:
            t_510 = self.dollar_parser(t_510)
            result += f"{self.splitter}{t_510}"
        return result

    def get_all_by_single_dollar(self, value: str, dollar:str) -> str:
        if not value:
            return
        result = ""
        for v_s in value.split(self.splitter):
            try:
                self.get_single_dollar(v_s, dollar)
            except:
                pass
        return result

    '''
    MON:
    '''

    def mon_per_id(self, value:str) -> str:
        if not value:
            return
        result = self.get_single_dollar(value, "0")
        if result:
            return result
        
    @property
    def purgue(self):
        res_json = self.res_json
        args = self.args.copy()
        fields = args.pop("fields", None)
        limit = args.pop("limit", "1000")
        view = args.pop("view", False)
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
                return res_json
            field:str = f"{self.dataset}.{field.strip()}"
        if fields:
            result = ""
            for field in self.available_fields:
                if field in fields.split(","):
                    result += f",{self.dataset}.{field}"
                else:
                    result += f",NULL"
            res_json["fields"] = result[1:]
        else:
            res_json["fields"] = fields
        
        not_available_field = next(filter(lambda kv: kv[0] not in self.available_fields, args.items()), None)
        if not_available_field:
            res_json["message"] = f"This field doesn't exist in the db: {not_available_field[0]}  - available fields: {self.available_fields}"
            return res_json
        if view:
            if view == "marc":
                res_json["fields"] = self.marc_fields
            elif view == "human":
                res_json["fields"] = self.human_fields
        res_json["args"] = args
        res_json["success"] = True
        return res_json
    
    def where(self, args: dict) -> str:
        args = dict(args)
        if not args:
            return ""
        result = "WHERE "
        and_or = " AND "
        for k,value in args:

            '''
            VIRTUAL START
            '''
            if k in self.virtual_fields:
                print(k.center(100,"#"))
                v = re.sub("\|\||¬|!", "", value)
                v_where = f''' {self.dataset}_fts match '{k}:NEAR("{v}")'  {and_or}'''
                result += v_where
            else:
                value: str = value.lower()
                if value[-2:] == "||":
                    and_or = " OR  "
                    value = value[0:-2]
                else:
                    and_or = " AND "
                if value[0] == "!":
                    value = value.replace("!", "NOT LIKE ", 1)
                else:
                    value = f"LIKE {value}"
                
                value = value.replace("||", f" OR {k} LIKE ")
                value = value.replace("¬", f" AND {k} LIKE ")
                value = value.replace("LIKE !", "NOT LIKE ")
                value_splitted = value.split(" ")
                for v in value_splitted:
                    if v.islower() and v not in self.available_fields or not v.isalnum():
                        if v == "null":
                            value = value.replace(v, "NULL")
                            if value.find("NOT LIKE NULL") >= 0:
                                value = value.replace("NOT LIKE NULL", "IS NOT NULL")
                            elif value.find("LIKE NULL") >= 0:
                                value = value.replace("LIKE NULL", "IS NULL")
                        else:
                            if k.startswith("t_"):
                                value = value.replace(v, f"'|%{v}%'")
                            else:
                                value = value.replace(v, f"'%{v}%'")

                result += f"{k} {value}{and_or}"
        return result[0:-5]
    
    def fts_add(self,args:list) -> str:
        result = ""
        for k in args:
            if k in self.virtual_fields:
                result = f''' INNER JOIN {self.dataset}_fts ON {self.dataset}_fts.id = {self.dataset}.id '''
        return result

    def query(self) -> dict:
        
        res_json = self.purgue
        if not res_json["success"]:
            return {"success":False,"message":res_json["message"]}
        
        all_fields=""
        for field in self.available_fields:
            all_fields += f"{self.dataset}.{field}, "
        fields = res_json['fields'] if res_json['fields'] else all_fields[0:-2] #TODO: put all fields after and make always the conversion to -> dataset.field
        query = f"SELECT {fields} FROM {self.dataset} "
        query += self.fts_add(res_json["args"].keys())
        query += self.where(res_json["args"].items())
        query += f" LIMIT {res_json['limit']};"
        print(f"\n{query}\n".center(50 + len(query),"#"))
        res = self.cur.execute(query)
        res_json = self.res_json
        res_json["success"] = True
        print(self.dataset)
        res_json["data"] = map(lambda row:structs[self.dataset](*row),res)
        # res_json["data"] = map(lambda row:dict(zip(a_f,row)),res)
        return res_json
    
    def blunt_query(self):
        start = self.time
        query: str = self.args.get("query")
        res_json = self.res_json
        blacklisted = ("update", "delete", "create", "insert", "pragma", "table_info", "drop", "alter" , "commit", "into")
        if query:
            q = query.lower()
            for bl in blacklisted:
                if q.find(bl) >= 0:
                    res_json["message"] = "Not a valid query"
                    return res_json
        print(query)
        try:
            # res = list(self.cur.execute(query))
            def xxx(row):
                print(row)
            res = self.cur.execute(query)
        except Exception as e:
            res_json["message"] = "Bad formulated query"
            res_json["error"] = f"{e}"
            return res_json
        res_json["success"] = True
        res_json["data"] = res
        return res_json

    def insert(self):
        res_json = {"success":False}
        with open(f"converter/{self.dataset}.json", mode="rb") as file:
            try:
                data = msgspec.json.decode(file.read())
                query = f"insert or ignore into {self.dataset} values ({'?, '*len(self.available_fields)})"
                query = query.replace(", )", ")")
                print(query.center(50 + len(query), "#"))
                self.cur.executemany(query,map(lambda record: self.extract_values(self.dataset, record), data))
                self.con.commit()
                res_json["success"] = True
                return res_json
            except Exception as e:
                res_json["message"] = f"{e}"
                return res_json