import requests
import json
data = {
    "assetnummer": "W127",
    "storing" : 0,
    "druk_a1" :  0,
    "druk_a2" :  0,
    "druk_b1" : 0,
    "druk_b2" : 0,
    "kracht_a" : 0,
    "kracht_b" : 0,
    "omloop_a" : 0,
    "omloop_b" : 0,
} 
r = requests.post(url = "http://10.165.2.10:8000/tram/insertlogodata", data = data)

print(r.json().get("response"))

