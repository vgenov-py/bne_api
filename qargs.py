from constants import DB_FILE
import sqlite3
from flask import g
import re
import msgspec
from typing import Optional

class Qargs:
    '''
    Qargs (Query from args)
    This object will create a valid sqlite3 SELECT query based on args supplied
    args have to be previously curated
    args can contain one or more of the followings:
    table:str
    fields:[[]str]
    filters: [k=v,...]|None
    join: [k:v,...]|None
    limit:int|1000
    '''
    def __init__(self,args:dict) -> None:
        self.args = args

    @property
    def cur(self):
        return sqlite3.connect(DB_FILE)
    
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
    def available_fields(self) -> tuple:
        result = (f"{self.table}.{row[1]}" for row in self.cur.execute(f"pragma table_info({self.table});"))
        return tuple(result)
    


if __name__ == "__main__":
    import os
    os.system("python3 test_qargs.py")