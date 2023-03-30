import csv


with open("enrichment/001s.csv", "r", encoding="utf-8", errors="ignore") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    next(csv_reader)
    csv_reader = tuple(csv_reader)
    csv_2021 = tuple(map(lambda row: row[0].strip(), csv_reader))
    csv_2023 = tuple(map(lambda row: row[1].strip(), csv_reader))
    with open("enrichment/001s_proccessed.csv","w" ,encoding="utf-8") as w_file:
        csv_writer = csv.writer(w_file, delimiter=";")
        csv_writer.writerow(("ids 2021 inexistentes en 2023", "ids 2023 inexistentes en 2021"))
        to_write_2021 = []
        to_write_2023 = []
        for i, id in enumerate(csv_2021):
            if id not in csv_2023:
                to_write_2021.append(id)
        for id in csv_2023:
            if id not in csv_2021:
                to_write_2023.append(id)
        csv_writer.writerows(zip(to_write_2021, to_write_2023))