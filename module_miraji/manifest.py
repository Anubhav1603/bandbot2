import csv
import json

json_data = {"name": "images", "data": []}

file_lst = json_data["data"]

with open("images/miraji_dict.csv", mode="r", encoding="utf-8") as f:
    fc = csv.reader(f)
    fclst = list(fc)

for elem in fclst:
    tup = (elem[1][7:], False)
    file_lst.append(tup)

tup = ("miraji_dict.csv", True)
file_lst.append(tup)

with open("manifest.json", "w") as json_file:
    json.dump(json_data, json_file, indent = 4)