import requests
import json
import datetime
import time
import concurrent.futures

data2 = b'{"ojson":{"assetnummer":"Michiel","storing":256,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":3,"omloop_b":1,"kracht_a":0,"kracht_b":0}}'

print(f"==========POSTGRES========")
aantallen = [1, 10, 100, 1000, 10000]

def insert_data(aantal):
    print(f"==========Opdracht gestart: {aantal} maal data invoeren.========")
    voor = datetime.datetime.now()
    for i in range (0, aantal):
        r = requests.post(url = "http://127.0.0.1:8000/tram/insertlogodata", data = data2)
    na = datetime.datetime.now()
    verschil = na - voor

    output = f"{verschil.microseconds / 1000} miliseconden" if verschil.seconds < 2 else f"{verschil.seconds} seconden"
    print(f"==========Klaar. Opdracht duurde {output}.==========")
    print("\n")

def insert_data_blanco(aantal):
    for i in range (0, aantal):
        r = requests.post(url = "http://127.0.0.1:8000/tram/insertlogodata", data = data2)


def get_data(aantal):
    print(f"==========Opdracht gestart: data ophalen.========")
    voor = datetime.datetime.now()
    for i in range (0, aantal):
        r = requests.get(url = "http://127.0.0.1:8000/tram/api/get_sensor_waarden/Michiel/omloop_a", data = data2)
    na = datetime.datetime.now()
    verschil = na - voor

    output = f"{verschil.microseconds / 1000} miliseconden" if verschil.seconds < 2 else f"{verschil.seconds} seconden"
    print(f"==========Klaar. Opdracht duurde {output}. Aantal ontvangen objecten: {len(r.json())}==========")

def cooldown():
    print("\n \n \n")
    time.sleep(15)

def multiprocessing(aantal):
    print(f"==========Opdracht gestart: {aantal} maal date GELIJKTIJDIG invoeren.========")
    voor = datetime.datetime.now()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(insert_data_blanco, 1) for _ in range(aantal)]
        for f in concurrent.futures.as_completed(results):
            f.result()
    na = datetime.datetime.now()
    verschil = na - voor
    output = f"{verschil.microseconds / 1000} miliseconden" if verschil.seconds < 2 else f"{verschil.seconds} seconden"
    print(f"==========Klaar. Opdracht duurde {output}.==========")

if __name__ == "__main__":
    multiprocessing(100)
    # for x in aantallen:
    #     insert_data(x)
    #     get_data(1)
    #     cooldown()