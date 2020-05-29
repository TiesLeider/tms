import requests
import json
import datetime
import random
import concurrent.futures

assets = ["w2641", "w300", "w563", "w691", "w971"]
assets_nums = ["2641", "W300", "W563", "W691", "W971"]
storingen = [0,0,0,0,0,0,4,8,256,1024]
omlopen = [0,0,1,1,3,4,5]


def genereer_json_object():
    obj = '{"ojson":{"assetnummer":"'+ random.choice(assets) +'","storing":'+ str(random.choice(storingen)) +',"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":'+ str(random.choice(omlopen)) +',"omloop_b":1,"kracht_a":0,"kracht_b":0}}'
    return obj.encode()

def push_data():
    r = requests.post(url = "http://127.0.0.1:8000/tram/insertlogodata", data = genereer_json_object())

def multiprocessing(aantal):
    uitvoeringen = 20000
    print(f"==========Start. aantal={aantal*uitvoeringen}.==========")
    voor = datetime.datetime.now()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(push_data) for _ in range(uitvoeringen)]
        for f in concurrent.futures.as_completed(results):
            f.result()
    na = datetime.datetime.now()
    verschil = na - voor
    output = f"{verschil.microseconds / 1000} miliseconden" if verschil.seconds < 2 else f"{verschil.seconds} seconden"
    with open("db_test.txt", "a+") as outfile:
        outfile.write(f"==========Klaar. aantal regels={aantal*uitvoeringen} Opdracht duurde {verschil.seconds / 60} minuten.==========\n")
    print(f"==========Klaar. aantal regels={aantal*uitvoeringen} Opdracht duurde gemiddeld {verschil.seconds / 60} minuten. ==========")

def get_data(assets, aantal):
    print(f"==========Opdracht gestart: data ophalen.========")
    voor = datetime.datetime.now()
    for asset in assets:
        r = requests.get(url = f"http://127.0.0.1:8000/tram/api/get_sensor_waarden_oud/{asset}/omloop_a")
    na = datetime.datetime.now()
    verschil = na - voor

    totaal_ms = (verschil.seconds * 1000) + (verschil.microseconds / 1000)

    output = f"{verschil.microseconds / 1000} miliseconden" if verschil.seconds < 2 else f"{verschil.seconds} seconden"
    print(f"==========Klaar. Opdracht duurde {output}. Aantal ontvangen objecten: {len(r.json())}==========")
    with open("database_resultaten.csv", "a+") as csv_outfile:
        csv_outfile.write(f"{(aantal * 20000)+500000}, {totaal_ms}, {totaal_ms / 5}\n")




if __name__ == "__main__":
    with open("database_resultaten.csv", "a+") as csv_outfile:
            csv_outfile.write(f"aantal_rijen, tijdsduur(ms), gemiddelde_tijdsduur(ms) \n")
    for i in range(25,101):
        multiprocessing(i)
        get_data(assets_nums, i)
