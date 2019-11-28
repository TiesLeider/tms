import requests
import json
data = b'{"ojson":{"assetnummer":"w559","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":13,"omloop_b":1,"kracht_a":0,"kracht_b":0}}'
data2 = b'{"ojson":{"assetnummer":"Michiel","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":12,"omloop_b":1,"kracht_a":0,"kracht_b":0}}'
data3 = b'{"ojson":{"assetnummer":"w490","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":14,"omloop_b":1,"kracht_a":0,"kracht_b":0}}'
data4 = b'{"ojson":{"assetnummer":"w2642","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":14,"omloop_b":1,"kracht_a":0,"kracht_b":0}}'

# r = requests.post(url = "http://10.165.2.10:8000/tram/insertlogodata", data = data)

for i in range(0, 5):
    r = requests.post(url = "http://127.0.0.1:8000/tram/insertlogodata", data = data)
    s = requests.post(url = "http://127.0.0.1:8000/tram/insertlogodata", data = data2)
    t = requests.post(url = "http://127.0.0.1:8000/tram/insertlogodata", data = data3)
    u = requests.post(url = "http://127.0.0.1:8000/tram/insertlogodata", data = data4)
    print(f"{i} : \n {r.json()} \n {s.json()} \n {t.json()} \n {u.json()} \n ============================================ ")
