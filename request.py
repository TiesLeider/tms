import requests
import json
import datetime
data = b'{"ojson":{"assetnummer":"Michiel","storing":0,"druk_b1":0,"druk_b2":0,"druk_a1":420,"druk_a2":0,"omloop_a":10,"omloop_b":1,"kracht_a":0,"kracht_b":0}}'
data2 = b'{"ojson":{"assetnummer":"Michiel","storing":256,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":3,"omloop_b":1,"kracht_a":0,"kracht_b":0}}'
data3 = b'{"ojson":{"assetnummer":"w490","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":7,"omloop_b":1,"kracht_a":0,"kracht_b":0}}'
data4 = b'{"ojson":{"assetnummer":"w2641","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":11,"omloop_b":1,"kracht_a":0,"kracht_b":0}}'

data5 = b'{"ojson": { "received" : "2019-12-15 15:04:12", "modem": "wwan0", "from": "+3197023127984", "omschrijving": "Tongen Bak A+B defect", "smsc": "+31624000045", "udh": "false", "input": "2", "status": "Idle", "alphabet": "ISO", "sent": "2019-12-15 15:04:05",  "sim": "sim0", "wissel": "W309-311"}}'
data6 = b'''{"ojson":{ "received": "2019-12-16 22:13:01", "modem": "wwan0", "from": "+3197023127984", "omschrijving": "Tongen Bak A+B defect", "smsc": "+31624000045",
"udh": "false",
"input": "2",
"status": "Active",
"alphabet": "ISO",
"sent": "2019-12-16 22:12:57",
"sim": "sim0",
"wissel": "W309-311"
 }
}'''


# r = requests.post(url= "http://127.0.0.1:8000/tram/insertlogodata", data=data2)
# print(r.json())

voor = datetime.datetime.now()
for i in range (0, 1):
    r = requests.post(url = "http://10.165.2.10:8000/tram/insertlogodata", data = data2)
na = datetime.datetime.now()
verschil = na - voor

output = f"{verschil.microseconds / 1000} miliseconden" if verschil.seconds < 2 else f"{verschil.seconds} seconden"
print(f"==========Klaar. Opdracht duurde {output}==========")



# # print(f"{r.json()}")

# pompdata = b'{"ojson":{"assetnummer":"pomp1","storing":2,"niveau":0}}'

# r = requests.post( url="http://10.165.2.10:8000/pomp/insertdata", data = pompdata)