from django.db import models
import pymongo
import bson.objectid as objectid
import datetime
import uuid

client = pymongo.MongoClient("mongodb://localhost:27017")

db = client["tms"]
asset_col = db["tram_asset"]
config_col = db["tram_configuratie"]
logo_col = db["tram_logodata"]
univos_col = db["tram_urgentieniveau"]

niv_data = [
    {"_id": objectid.ObjectId(), "niveau": 0, "beschrijving": "Geen Actie"},
    {"_id": objectid.ObjectId(), "niveau": 1, "beschrijving": "Licht"},
    {"_id": objectid.ObjectId(), "niveau": 2, "beschrijving": "Gemiddeld"},
    {"_id": objectid.ObjectId(), "niveau": 3, "beschrijving": "Zwaar"},
    {"_id": objectid.ObjectId(), "niveau": 4, "beschrijving": "Direct"},
]

univos_col.insert_many(niv_data)


ell_stand1 = [
    {"_id":objectid.ObjectId(),
    "naam":"ELL-standaard",
    "config":[
        {"inputnummer":1,"signaaltype":"analoog","beschrijving":"Druk/Kracht (oil) point A","urgentieniveau_id":0},
        {"inputnummer":2,"signaaltype":"pulse","beschrijving":"Druk/Kracht (force) point A","urgentieniveau_id":0},
        {"inputnummer":3,"signaaltype":"digitaal","beschrijving":"No Fail Save","urgentieniveau_id":4},
        {"inputnummer":4,"signaaltype":"digitaal","beschrijving":"Tongen failure A+B","urgentieniveau_id":2},
        {"inputnummer":5,"signaaltype":"digitaal","beschrijving":"Volgorde","urgentieniveau_id":2},
        {"inputnummer":6,"signaaltype":"digitaal","beschrijving":"WSA Defect","urgentieniveau_id":2},
        {"inputnummer":7,"signaaltype":"analoog","beschrijving":"Druk/kracht (oil) point B","urgentieniveau_id":0},
        {"inputnummer":8,"signaaltype":"pulse","beschrijving":"Druk/kracht (force) point B","urgentieniveau_id":0},
        {"inputnummer":9,"signaaltype":"digitaal","beschrijving":"Timeout L of R point A of Point B","urgentieniveau_id":2},
        {"inputnummer":10,"signaaltype":"digitaal","beschrijving":"Verzamelmelding deksels, water in bak","urgentieniveau_id":4},
        {"inputnummer":11,"signaaltype":"digitaal","beschrijving":"omloopteller bak A","urgentieniveau_id":0},
        {"inputnummer":12,"signaaltype":"digitaal","beschrijving":"omloopteller bak B","urgentieniveau_id":0},

        ]
    },
        {"_id":objectid.ObjectId(),
    "naam":"Amstelveen",
    "config":[
        {"inputnummer":1,"signaaltype":"analoog","beschrijving":"Druk/Kracht (oil) point A Links","urgentieniveau_id":0},
        {"inputnummer":2,"signaaltype":"pulse","beschrijving":"Druk/Kracht (force) point A Rechts","urgentieniveau_id":0},
        {"inputnummer":3,"signaaltype":"digitaal","beschrijving":"No Fail Save","urgentieniveau_id":4},
        {"inputnummer":4,"signaaltype":"digitaal","beschrijving":"Tongen failure A+B","urgentieniveau_id":2},
        {"inputnummer":5,"signaaltype":"digitaal","beschrijving":"Volgorde","urgentieniveau_id":2},
        {"inputnummer":6,"signaaltype":"digitaal","beschrijving":"WSA Defect","urgentieniveau_id":2},
        {"inputnummer":7,"signaaltype":"digitaal","beschrijving":"Open gereden","urgentieniveau_id":3},
        {"inputnummer":8,"signaaltype":"digitaal","beschrijving":"Reserve","urgentieniveau_id":0},
        {"inputnummer":9,"signaaltype":"digitaal","beschrijving":"Timeout L of R point A of Point B","urgentieniveau_id":2},
        {"inputnummer":10,"signaaltype":"digitaal","beschrijving":"Verzamelmelding deksels, water in bak","urgentieniveau_id":4},
        {"inputnummer":11,"signaaltype":"digitaal","beschrijving":"omloopteller bak A","urgentieniveau_id":0},
        {"inputnummer":12,"signaaltype":"digitaal","beschrijving":"omloopteller bak B","urgentieniveau_id":0},

        ]
    },
        {"_id":objectid.ObjectId(),
    "naam":"H&K-Standaard",
    "config":[
        {"inputnummer":1,"signaaltype":"analoog","beschrijving":"Druk/Kracht (oil) point A","urgentieniveau_id":0},
        {"inputnummer":2,"signaaltype":"analoog","beschrijving":"Druk/Kracht (force) point A","urgentieniveau_id":0},
        {"inputnummer":3,"signaaltype":"digitaal","beschrijving":"No Fail Save","urgentieniveau_id":4},
        {"inputnummer":4,"signaaltype":"digitaal","beschrijving":"Tongen failure A+B","urgentieniveau_id":2},
        {"inputnummer":5,"signaaltype":"digitaal","beschrijving":"Volgorde","urgentieniveau_id":2},
        {"inputnummer":6,"signaaltype":"digitaal","beschrijving":"WSA Defect","urgentieniveau_id":2},
        {"inputnummer":7,"signaaltype":"analoog","beschrijving":"Druk/kracht (oil) point B","urgentieniveau_id":0},
        {"inputnummer":8,"signaaltype":"analoog","beschrijving":"Druk/kracht (force) point B","urgentieniveau_id":0},
        {"inputnummer":9,"signaaltype":"digitaal","beschrijving":"Timeout L of R point A of Point B","urgentieniveau_id":2},
        {"inputnummer":10,"signaaltype":"digitaal","beschrijving":"Verzamelmelding deksels, water in bak","urgentieniveau_id":4},
        {"inputnummer":11,"signaaltype":"digitaal","beschrijving":"omloopteller bak A","urgentieniveau_id":0},
        {"inputnummer":12,"signaaltype":"digitaal","beschrijving":"omloopteller bak B","urgentieniveau_id":0},

        ]
    },


]

# data1 = {"bool": True, "int": int(35), "float": float(37.381), "hex": hex(44)}
print(hex(255))

logo_col.insert_one({
    "assetnummer_id": "W001",
    "tijdstip": datetime.datetime.now(),
    "druk_a1": 0x0,
    "druk_a2": 0x0,
    "druk_b1": 0x0,
    "druk_b2": 0x0,
    "kracht_a": 0x0,
    "kracht_b": 0x0,
    "omloop_a": 0x3fa,
    "omloop_b": 0x0,
    "storing": 0x2004,

})


# logo_col.insert_one(data1)

config_col.insert_many(ell_stand1)

# for configur in ell_stand:
#     # print(configur)
#     configlijst_col.insert_one(configur)