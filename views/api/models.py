from db import db
import re

class Geo(db.Model):
    __tablename__ = "geographic"
    id = db.Column(db.String(10), primary_key=True)
    t_003 = db.Column(db.String(10))
    t_005 = db.Column(db.String(32))
    t_008 = db.Column(db.String(62))
    t_010 = db.Column(db.String(32))
    t_016 = db.Column(db.String(32))
    t_024 = db.Column(db.String(200))
    t_034 = db.Column(db.String(100))
    t_040 = db.Column(db.String(100))
    t_042 = db.Column(db.String(100))
    t_080 = db.Column(db.String(100))
    t_151 = db.Column(db.String(255))
    t_550 = db.Column(db.String(100))
    t_670 = db.Column(db.String(255))
    t_781 = db.Column(db.String(100))
    lat_lng = db.Column(db.String(100))

    def __init__(self, record:dict) -> None:
        self.id = record.get("001")
        self.t_003 = record.get("003")
        self.t_005 = record.get("005")
        self.t_008 = record.get("008")
        self.t_010 = record.get("010")
        self.t_016 = record.get("016")
        self.t_024 = record.get("024")
        self.t_034 = record.get("034")
        self.t_040 = record.get("040")
        self.t_042 = record.get("042")
        self.t_080 = record.get("080")
        self.t_151 = record.get("151")
        self.t_550 = record.get("550")
        self.t_670 = record.get("670")
        self.t_781 = record.get("781")
        self.lat_lng = self.f_lat_lng(record.get("034")) if self.f_lat_lng(record.get("034")) else None

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

    def __str__(self) -> str:
        result = {}
        result["001"] = self.id
        result["670"] = self.t_670
        return str(result)
    def __repr__(self) -> str:
        result = {}
        result["001"] = self.id
        result["670"] = self.t_670
        return str(result)
    
    def public(self):
        result = {}
        result["ID_BNE"] = self.id
        result["Descripción"] = self.t_670
        result["Coordenadas"] = self.t_034
        return result
    
class Per(db.Model):
    __tablename__ = "person"
    id = db.Column(db.String(10), primary_key=True)
    t_003 = db.Column(db.String(255))
    t_005 = db.Column(db.String(255))
    t_008 = db.Column(db.String(255))
    t_024 = db.Column(db.String(255))
    t_046 = db.Column(db.String(255))
    t_100 = db.Column(db.String(255))
    t_368 = db.Column(db.String(255))
    t_370 = db.Column(db.String(255))
    t_372 = db.Column(db.String(255))
    t_373 = db.Column(db.String(255))
    t_374 = db.Column(db.String(255))
    t_375 = db.Column(db.String(255))
    t_377 = db.Column(db.String(255))
    t_400 = db.Column(db.String(255))
    t_500 = db.Column(db.String(255))
    t_670 = db.Column(db.String(255))

    def __init__(self, record:dict) -> None:
        self.id = record.get("001")
        self.t_003 = record.get("003")
        self.t_003 = record.get("003")
        self.t_005 = record.get("005")
        self.t_008 = record.get("008")
        self.t_024 = record.get("024")
        self.t_046 = record.get("046")
        self.t_100 = record.get("100")
        self.t_400 = record.get("400")
        self.t_368 = record.get("368")
        self.t_370 = record.get("370")
        self.t_372 = record.get("372")
        self.t_373 = record.get("373")
        self.t_374 = record.get("374")
        self.t_375 = record.get("375")
        self.t_377 = record.get("377")
        self.t_500 = record.get("500")
        self.t_670 = record.get("670")

    def public(self):
        result = {}
        result["ID_BNE"] = self.id
        result["Fuentes"] = self.t_670
        result["Nombre"] = self.t_100
        result["Género"] = self.t_375
        result["Mas cosas"] = f"{self.t_370} {self.t_375} {self.t_368} {self.t_500} {self.t_024}"
        return result
    def __str__(self) -> str:
        result = {}
        result["001"] = self.id
        result["670"] = self.t_670
        return str(result)
    def __repr__(self) -> str:
        result = {}
        result["001"] = self.id
        result["670"] = self.t_670
        return str(result)
    