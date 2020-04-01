from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Sum, Avg
from ..models import *
from .polling import LogoPolling, SmsPolling, LogoData
from requests.exceptions import Timeout
import requests
import traceback
import datetime
import json
import logging
import subprocess
import platform
import os
from django.template import Context, loader

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', filename="api.log", level=logging.INFO)


def requesthandler(request):
    if (request.body == "" or not request.body):
        return JsonResponse({"response": False, "error":  "POST inhoud niet aangekomen."})
    else:
        return request


@csrf_exempt
def insert_logo_data(request):
    try:
        # Check of de requestdata ok is en manipuleer assetnummer:
        requesthandler(request)
        data = str(request.body)[2:-1]
        json_data = json.loads(data).get("ojson")
        assetnummer = json_data.get("assetnummer").upper() if json_data.get(
            "assetnummer").startswith("w") else json_data.get("assetnummer")
        if len(assetnummer) > 4 and assetnummer.startswith("W"):
            assetnummer = assetnummer[1:]
        asset = Asset.objects.select_related("laatste_data").get(assetnummer=assetnummer)
        # Maak record Logodata:
        record = LogoData(json_data, asset)
        if asset.laatste_data:
            if ( record.storing == 0 and  
                asset.druk_a1 == record.druk_a1 and
                asset.druk_a2 == record.druk_a2 and
                asset.druk_b1 == record.druk_b1 and
                asset.druk_b2 == record.druk_b2 and
                asset.kracht_a == record.kracht_a and
                asset.kracht_b == record.kracht_b and
                record.omloop_a == 0 and 
                record.omloop_b == 0
                ):
                asset.laatste_data.save()
                return JsonResponse({"response": True, "error": None})
                logging.error(f"{assetnummer}: polling overgeslagen. Identieke polling.")
            elif (asset.laatste_data.omloop_a_toegevoegd > 25 and asset.laatste_data.omloop_a_toegevoegd == record.omloop_a and
                asset.laatste_data.omloop_b_toegevoegd == record.omloop_b):
                asset.laatste_data.save()
                return JsonResponse({"response": True, "error": None})
                logging.error(f"{assetnummer}: polling overgeslagen. Identieke polling.")
            else:
                pass


        polling = LogoPolling(logo_data=record, asset=asset)
        polling.insert_absolute_data()
        polling.storing_algoritme()

        return JsonResponse({"response": True, "error": None})
    except Exception as ex:
        traceback.print_exc()
        logging.error("%s", traceback.format_exc())
        return JsonResponse({"response": False, "error": str(ex), "type": str(type(ex))})


@csrf_exempt
def insert_sms_data(request):
    try:
        requesthandler(request)
        data = str(request.body)[2:-1]
        json_data = json.loads(data).get("ojson")
        sms_polling = SmsPolling(json_data)
        #sms_polling.insert_sms_data()
        return JsonResponse({"response": True, "error": None})
    except Exception as ex:
        traceback.print_exc()
        logging.error(" %s", traceback.format_exc())
        return JsonResponse({"response": False, "error": str(ex), "type": str(type(ex))})


def get_actieve_storingen(request):
    storingen_qs = Storing.objects.filter(
        actief=True, gezien=False)
    data = list(storingen_qs.values("id", "assetnummer__beschrijving", "assetnummer__assetnummer",
                                    "bericht", "som", "score", "laatste_data__omloop_a", "laatste_data__omloop_b", "laatste_data__tijdstip"))

    for item in data:
        try:
            item["laatste_data__isotijdstip"] = item["laatste_data__tijdstip"].isoformat() 
            item["laatste_data__tijdstip"] = item["laatste_data__tijdstip"].strftime(   
                "%d %b %Y, %H:%M")
        except AttributeError:
            item["laatste_data__isotijdstip"] = ""
            item["laatste_data__tijdstip"] = "<i>Tijdstip en omlopen worden geüpdatet bij een nieuw alarm</i>"
            item["laatste_data__omloop_a"] = "-"
            item["laatste_data__omloop_b"] = 0

    return JsonResponse(data, safe=False)


def get_sms_data(request):
    sms_qs = SmsData.objects.all().order_by("-ontvangen")
    data = list(sms_qs.values("ontvangen", "telnummer",
                              "storing", "status", "asset"))

    return JsonResponse(data, safe=False)


def index_form(request):
    if request.method == "POST":
        data = str(request.body)[2:-1]
        json_data = json.loads(data).get("geselecteerde_storingen")

        for sid in json_data:
            storing = get_object_or_404(Storing, pk=sid)
            storing.gezien = True
            if json.loads(data).get("method") == "herstellen":
                storing.actief = False
            storing.save()

        return HttpResponse(request.POST.dict())
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def check_assets_online_oud(request):
    try:
        online_assets = Asset.objects.filter(pollbaar=True)
        offline_assets = []
        for asset in online_assets:
            ad = AbsoluteData.objects.filter(assetnummer=asset).latest()
            if (ad.tijdstip < (datetime.datetime.now() - datetime.timedelta(minutes=30))):
                offline_assets.append(
                    {"assetnummer": asset.assetnummer, "tijdstip": ad.tijdstip.strftime("%d %b %Y, %H:%M")})
    except Exception as ex:
        traceback.print_exc()
        logging.error("%s", traceback.format_exc())

    return JsonResponse(offline_assets, safe=False)


# def check_online_assets(request):
#     def ping(host):
#         FNULL = open(os.devnull, 'w')
#         param = '-n' if platform.system().lower() == 'windows' else '-c'
#         return subprocess.call(
#             ["ping", param, "1", host], stdout=FNULL) == 0

#     try:
#         logo_assets = Asset.objects.exclude(ip_adres_logo=None)
#         offline_assets = []
#         for asset in logo_assets:
#             # if ping(asset.ip_adres_logo) != 0:
#             try:
#                 r = requests.get(f"http://{asset.ip_adres_logo}/", timeout=3)
#             except Timeout:
#                 try:
#                     ad = AbsoluteData.objects.filter(
#                         assetnummer=asset).latest()
#                     tijdstip = ad.tijdstip.strftime("%d %b %Y, %H:%M")
#                 except ObjectDoesNotExist:
#                     tijdstip = "Nooit"
#                 offline_assets.append(
#                     {"assetnummer": asset.assetnummer, "tijdstip": tijdstip})
#     except Exception as ex:   
#         traceback.print_exc()
#         logging.error("%s", traceback.format_exc())

#     return JsonResponse(offline_assets, safe=False)

def check_online_assets(request):
    r = requests.get("http://10.165.2.10:1810/api/getLive")
    offline_assets = []
    for asset in r.json():
            for key, value in asset.items():
                if value == False:
                    assetnummer = key.upper() if key.startswith("w") else key
                    if len(assetnummer) > 4 and assetnummer.startswith("W"):
                        assetnummer = assetnummer[1:]
                    asset = Asset.objects.select_related("laatste_data").get(assetnummer=assetnummer)
                    try:
                        tijdstip = asset.laatste_data.tijdstip.strftime("%d %b %Y, %H:%M")
                    except:
                        tijdstip = "Nooit"
                    if asset.pollbaar == True:
                        offline_assets.append(
                            {"assetnummer": asset.assetnummer, "tijdstip": tijdstip})
    return JsonResponse(offline_assets, safe=False)


def get_sensor_waarden_oud(request, assetnummer, veld):
    qs = AbsoluteData.objects.filter(assetnummer=assetnummer).order_by("tijdstip")
    data = list(qs.values(veld, "tijdstip"))
    response = []
    for item in data:
        response.append( [round(item["tijdstip"].timestamp()) * 1000, item[veld]])


    return JsonResponse(response, safe=False)

def get_sensor_waarden(request, assetnummer, veld):
    #TODO append met de database_data

    return HttpResponse(loader.get_template(f"tram/data/{assetnummer}/{veld}.json").render())

def get_maand_gemiddelde(request, assetnummer, veld):
    nu = datetime.datetime.now()
    vorige_maand = nu - datetime.timedelta(days=30)
    vorige_week = nu - datetime.timedelta(days=7)
    gister = nu - datetime.timedelta(days=1)
    maand_qs = AbsoluteData.objects.filter(assetnummer=assetnummer, tijdstip__range=(vorige_maand, nu))
    week_qs = AbsoluteData.objects.filter(assetnummer=assetnummer, tijdstip__range=(vorige_week, nu))
    dag_qs = AbsoluteData.objects.filter(assetnummer=assetnummer, tijdstip__range=(gister, nu))
    maand_gemiddelde = maand_qs.aggregate(Avg(veld)).get(veld + "__avg") if maand_qs.count() > 0 else 0
    week_gemiddelde = week_qs.aggregate(Avg(veld)).get(veld + "__avg") if week_qs.count() > 0 else 0
    dag_gemiddelde = dag_qs.aggregate(Avg(veld)).get(veld + "__avg") if dag_qs.count() > 0 else 0
    


    response = {
        "maand_gemiddelde": round(maand_gemiddelde),
        "week_gemiddelde": round(week_gemiddelde),
        "dag_gemiddelde": round(dag_gemiddelde)
    }
    return JsonResponse(response)

def get_ipnummers(request):
    qs = Asset.objects.exclude(ip_adres_logo=None)
    return JsonResponse(list(qs.values("assetnummer", "ip_adres_logo")) , safe=False)
