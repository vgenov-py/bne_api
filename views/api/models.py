# from db import db
import re
from uuid import uuid4

query_create_geo = f'''
    CREATE TABLE geo (
        id TEXT PRIMARY KEY,
        t_001 TEXT,
        t_024 TEXT,
        t_034 TEXT,
        t_080 TEXT,
        t_151 TEXT,
        t_451 TEXT,
        t_510 TEXT,
        t_550 TEXT,
        t_551 TEXT,
        t_667 TEXT,
        t_670 TEXT,
        t_781 TEXT,
        id_BNE TEXT,
        otros_identificadores TEXT,
        coordenadas_lat_lng TEXT,
        CDU TEXT,
        nombre_de_lugar TEXT,
        otros_nombres_de_lugar TEXT,
        entidad_relacionada TEXT,
        materia_relacionada TEXT,
        lugar_relacionado TEXT,
        nota_general TEXT,
        fuentes_de_informacion TEXT,
        lugar_jerarquico TEXT,
        obras_relacionadas_en_el_catalogo_BNE TEXT
    );
'''

query_create_per = f'''
    CREATE TABLE per (
    id TEXT PRIMRAY KEY,
    t_001 TEXT,
    t_003 TEXT,
    t_005 TEXT,
    t_008 TEXT,
    t_024 TEXT,
    t_046 TEXT,
    t_100 TEXT,
    t_368 TEXT,
    t_370 TEXT,
    t_372 TEXT,
    t_373 TEXT,
    t_374 TEXT,
    t_375 TEXT,
    t_377 TEXT,
    t_400 TEXT,
    t_500 TEXT,
    t_670 TEXT
    );
'''

query_create_mon = f'''
    CREATE TABLE mon (
    id TEXT PRIMARY KEY,
    t_001 TEXT,
    t_035 TEXT,
    t_040 TEXT,
    t_100 TEXT,
    t_130 TEXT,
    t_245 TEXT,
    t_260 TEXT,
    t_300 TEXT,
    t_500 TEXT,
    t_899 TEXT,
    t_927 TEXT,
    t_980 TEXT,
    t_994 TEXT
    );
'''

class Mapper:

    @property
    def splitter(self):
        return " /**/ "

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

# class Geo(db.Model):
#     __tablename__ = "geo"
#     id = db.Column(db.String(10), primary_key=True)
#     t_003 = db.Column(db.String(10))
#     t_005 = db.Column(db.String(32))
#     t_008 = db.Column(db.String(62))
#     t_010 = db.Column(db.String(32))
#     t_016 = db.Column(db.String(32))
#     t_024 = db.Column(db.String(200))
#     t_034 = db.Column(db.String(100))
#     t_040 = db.Column(db.String(100))
#     t_042 = db.Column(db.String(100))
#     t_080 = db.Column(db.String(100))
#     t_151 = db.Column(db.String(255))
#     t_550 = db.Column(db.String(100))
#     t_670 = db.Column(db.String(255))
#     t_781 = db.Column(db.String(100))
#     lat_lng = db.Column(db.String(100))

#     def __init__(self, record:dict) -> None:
#         self.id = record.get("001")
#         self.t_003 = record.get("003")
#         self.t_005 = record.get("005")
#         self.t_008 = record.get("008")
#         self.t_010 = record.get("010")
#         self.t_016 = record.get("016")
#         self.t_024 = record.get("024")
#         self.t_034 = record.get("034")
#         self.t_040 = record.get("040")
#         self.t_042 = record.get("042")
#         self.t_080 = record.get("080")
#         self.t_151 = record.get("151")
#         self.t_550 = record.get("550")
#         self.t_670 = record.get("670")
#         self.t_781 = record.get("781")
#         self.lat_lng = self.f_lat_lng(record.get("034")) if self.f_lat_lng(record.get("034")) else None

#     def f_lat_lng(self, v):
#         re_coord = "\w{2}\d{1,}"
#         result = ""
#         try:
#             a = re.findall(re_coord, v)
#             for i, coord in enumerate(a):
#                 if i % 2 == 0:
#                     coord = coord[1:]
#                     c_point = coord[0]
#                     digits = coord[1:]
#                     n = float(f"{digits[0:3]}.{digits[3:]}")
#                     if c_point == "W" or c_point == "E":
#                         if c_point == "W":
#                             n = -n
#                         result += f"{n}"
#                     else:
#                         if c_point == "S":
#                             n = -n
#                         result += f", {n}"
        
#             return result
#         except:
#             return None

#     def __str__(self) -> str:
#         result = {}
#         result["001"] = self.id
#         result["670"] = self.t_670
#         return str(result)
#     def __repr__(self) -> str:
#         result = {}
#         result["001"] = self.id
#         result["670"] = self.t_670
#         return str(result)
    
#     def public(self):
#         result = {}
#         result["ID_BNE"] = self.id
#         result["Descripción"] = self.t_670
#         result["Coordenadas"] = self.t_034
#         return result
    
# class Per(db.Model):
#     __tablename__ = "per"
#     id = db.Column(db.String(10), primary_key=True)
#     t_003 = db.Column(db.String(255))
#     t_005 = db.Column(db.String(255))
#     t_008 = db.Column(db.String(255))
#     t_024 = db.Column(db.String(255))
#     t_046 = db.Column(db.String(255))
#     t_100 = db.Column(db.String(255))
#     t_368 = db.Column(db.String(255))
#     t_370 = db.Column(db.String(255))
#     t_372 = db.Column(db.String(255))
#     t_373 = db.Column(db.String(255))
#     t_374 = db.Column(db.String(255))
#     t_375 = db.Column(db.String(255))
#     t_377 = db.Column(db.String(255))
#     t_400 = db.Column(db.String(255))
#     t_500 = db.Column(db.String(255))
#     t_670 = db.Column(db.String(255))

#     def __init__(self, record:dict) -> None:
#         self.id = record.get("001")
#         self.t_003 = record.get("003")
#         self.t_003 = record.get("003")
#         self.t_005 = record.get("005")
#         self.t_008 = record.get("008")
#         self.t_024 = record.get("024")
#         self.t_046 = record.get("046")
#         self.t_100 = record.get("100")
#         self.t_400 = record.get("400")
#         self.t_368 = record.get("368")
#         self.t_370 = record.get("370")
#         self.t_372 = record.get("372")
#         self.t_373 = record.get("373")
#         self.t_374 = record.get("374")
#         self.t_375 = record.get("375")
#         self.t_377 = record.get("377")
#         self.t_500 = record.get("500")
#         self.t_670 = record.get("670")

#     def public(self):
#         result = {}
#         result["ID_BNE"] = self.id
#         result["Fuentes"] = self.t_670
#         result["Nombre"] = self.t_100
#         result["Género"] = self.t_375
#         result["Mas cosas"] = f"{self.t_370} {self.t_375} {self.t_368} {self.t_500} {self.t_024}"
#         return result
#     def __str__(self) -> str:
#         result = {}
#         result["001"] = self.id
#         result["670"] = self.t_670
#         return str(result)
#     def __repr__(self) -> str:
#         result = {}
#         result["001"] = self.id
#         result["670"] = self.t_670
#         return str(result)
    

    