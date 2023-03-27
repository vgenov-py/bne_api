import json
import os
from concurrent.futures import ThreadPoolExecutor

file_name = "converter/monomodernas003.txt"
file_to_write ="converter/monomodernas.json"

if __name__ == '__main__':
    import time
    start = time.perf_counter()
    file = open(file_name, encoding="utf-8", errors="ignore")
    # files = os.listdir("geo_parse")
    # files = map(lambda file: open(f"geo_parse/{file}"), files)
    result = []
    id_bne = None
    record = {}
    old_tag = None
    def mapper(line, old_tag=None):
        if line.find("DOCUMENT") >= 0:
            pass
        elif line.find("FORM=") >= 0:
            if record:
                result.append(record.copy())
                record.clear()
        try:
            t,v = line.split("|",1)
            v = f"|{v[0:-1]}"
            t = t[1:4]
            if old_tag == t:
                record[t] += f" /**/ {v}"
                return t
            record[t] = v
            return t
        except Exception as e:
            pass
            
    a = file.readlines()
    for line in a:
        old_tag = mapper(line, old_tag)
    file.close()
    file = open(file_to_write, "w", encoding="utf-8")
    json.dump(result, file, indent=4, ensure_ascii=False)
    file.close()

    finish = time.perf_counter()
    print(finish-start)