import requests
import json
data = b'{"ojson":{"assetnummer":"Michiel","storing":4,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":13,"omloop_b":0,"kracht_a":0,"kracht_b":0}}'

# r = requests.post(url = "http://10.165.2.10:8000/tram/insertlogodata", data = data)
r = requests.post(url = "http://127.0.0.1:8000/tram/insertlogodata", data = data)

print(r.json())


