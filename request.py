import requests
import json
data = b'{"ojson":{"assetnummer":"w559","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":5,"omloop_b":1,"kracht_a":0,"kracht_b":0}}'
data2 = b'{"ojson":{"assetnummer":"Michiel","storing":256,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":3,"omloop_b":1,"kracht_a":0,"kracht_b":0}}'
data3 = b'{"ojson":{"assetnummer":"w490","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":7,"omloop_b":1,"kracht_a":0,"kracht_b":0}}'
data4 = b'{"ojson":{"assetnummer":"w2642","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":11,"omloop_b":1,"kracht_a":0,"kracht_b":0}}'

data5 = b'{"ojson": { "received" : "2019-12-15 15:04:12", "modem": "wwan0", "from": "+3197023127984", "omschrijving": "Tongen Bak A+B defect", "smsc": "+31624000045", "udh": "false", "input": "2", "status": "Idle", "alphabet": "ISO", "sent": "2019-12-15 15:04:05",  "sim": "sim0", "wissel": "W309-311"}}'

# r = requests.post(url = "http://10.165.2.10:8000/tram/insertlogodata", data = data)

# for i in range(0, 1):
#     r = requests.post(url = "http://127.0.0.1:8000/tram/insertlogodata", data = data)
#     # s = requests.post(url = "http://127.0.0.1:8000/tram/insertlogodata", data = data2)
#     # t = requests.post(url = "http://127.0.0.1:8000/tram/insertlogodata", data = data3)
#     # u = requests.post(url = "http://127.0.0.1:8000/tram/insertlogodata", data = data4)
#     # print(f"{i} : \n {r.json()} \n {s.json()} \n {t.json()} \n {u.json()} \n ============================================ ")
#     print(f"{i} : \n {r.json()} \n ============================================ ")

r = requests.post(url= "http://127.0.0.1:8000/tram/insertsmsdata", data= data5)
print(f"{r.json()}")