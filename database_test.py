import requests
import json
import datetime
import random
import concurrent.futures

assets = ["w2641", "w300", "w563", "w691", "w971"]
storingen = [0,0,0,0,0,0,4,8,256,1024]
omlopen = [0,0,1,1,3,4,5]

def genereer_json_object():
    obj = '{"ojson":{"assetnummer":"'+ random.choice(assets) +'","storing":'+ random.choice(storingen) +',"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":'+ random.choice(omlopen) +',"omloop_b":1,"kracht_a":0,"kracht_b":0}}'.encode()
    return obj

def push_data():
    r = requests.post(url = "http://127.0.0.1:8000/tram/insertlogodata", data = genereer_json_object())

def multiprocessing(aantal):
    voor = datetime.datetime.now()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(push_data) for _ in range(100000)]
        for f in concurrent.futures.as_completed(results):
            f.result()
    na = datetime.datetime.now()
    verschil = na - voor
    output = f"{verschil.microseconds / 1000} miliseconden" if verschil.seconds < 2 else f"{verschil.seconds} seconden"
    with open("db_test.txt", "a+") as outfile:
        outfile.write(f"==========Klaar. aantal regels={aantal*100000} Opdracht duurde {output / 100000}.==========")

if __name__ == "__main__":
    for i in range(1,21):
        multiprocessing(i)
