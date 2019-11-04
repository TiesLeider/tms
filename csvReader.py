import csv
import pymongo
import bson.objectid as objectid
import datetime

client = pymongo.MongoClient("mongodb://localhost:27017")

db = client["tms"]
asset_col = db["tram_asset"]


with open('Wissels-IP.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    # print(csv_reader)
    # for row in csv_reader:
    #     print(row)
    try:
        for row in csv_reader:
                assetnummer = f"W{row[0]}" if (len(row[0]) < 4) else row[0]
                line_count += 1
                if row[0] != "":
                        asset_col.insert_one({"assetnummer": assetnummer, "beschrijving": row[2], "bevat_logo": True, "ip_adres": f"{row[1]}", "logo_online": False, "telefoonnummer": "geen", "configuratie_id": objectid.ObjectId("5dbfeab88a53e71396481a30"), "laatste_storing": 0, "aantal_omlopen": 0, "weging": 0, "laatste_update": datetime.datetime.now() })
    except Exception as e:
            print(e)
    print(f'Processed {line_count} lines.')