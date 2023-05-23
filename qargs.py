from constants import DB_FILE
import sqlite3
from flask import g
import re
import msgspec
from typing import Optional

class Qargs:
    '''
    Qargs (Query from args)
    This object will create a valid sqlite3 SELECT query based on args supplied\n
    args have to be previously curated\n
    args can contain one or more of the followings:\n
    table:str
    fields:[[]str]|None
    filters: {k:v,...}|None
    join: [k:v,...]|None
    limit:int|1000
    '''
    def __init__(self,model:str, args:dict) -> None:
        self.model = model
        self.pre_args = args

    @property
    def cur(self) -> sqlite3.Connection:
        return sqlite3.connect(DB_FILE)
    
    @property
    def args(self) -> dict:
        r = {}
        pre_args = self.pre_args.copy()
        r["table"] = self.model
        r["limit"] = pre_args.pop("limit", "1000")
        r["fields"] = pre_args.pop("fields", None)
        r["filters"] = pre_args
        return r
    
    @property
    def table(self) -> str:
        t:str = self.args.get("table")
        if not t:
            raise Exception("args must contain table.")
        return t
    
    @property
    def limit(self) -> int:
        limit:int = self.args.get("limit")
        try:
            int(limit)
        except:
            raise Exception("Limit must be an integer.")
        return int(limit)
    
    @property
    def fields(self) -> str:
        return self.args.get("fields")
    
    @property
    def filters(self) -> dict:
        return self.args.get("filters")
    
    @property
    def available_fields(self) -> tuple:
        result = (f"{self.table}.{row[1]}" for row in self.cur.execute(f"pragma table_info({self.table});"))
        return tuple(result)

    @property
    def select(self) -> str:
        result = "SELECT "
        if self.fields:
            result += self.fields
            return f"{result} FROM {self.table}"
        for field in self.available_fields:
            result += f"{field}, "
        return f"{result[:-2]} FROM {self.table}"
    
    @property
    def where(self) -> str:
        result = "WHERE "
        for k,v in self.filters.items():
            result += f"{self.table}.{k} LIKE '%{v}%' AND "
        return result[:-5]
    
    @property
    def query(self) -> str:
        result = f"{self.select} {self.where} LIMIT 1000;"
        return result

if __name__ == "__main__":
    import os
    os.system("python3 test_qargs.py")