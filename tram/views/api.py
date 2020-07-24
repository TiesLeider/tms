from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Sum, Avg, Count
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

def api_docs(request):
    return render(request, "tram/api_docs.html", {})

@csrf_exempt
def insert_logo_data(request):
    try:
        # Check of de requestdata ok is en manipuleer assetnummer:
        requesthandler(request)
        data = str(request.body)[2:-1]
        json_data = json.loads(data).get("ojson")
        assetnummer = json_data.get("assetnummer").upper() if json_data.get(
            "assetnummer").startswith("w") or json_data.get("assetnummer").startswith("v") or json_data.get("assetnummer").startswith("s") else json_data.get("assetnummer")
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
        logging.info(f"==================={str(request.body)[2:-1]}=================")
        logging.error("%s", traceback.format_exc())
        return JsonResponse({"response": False, "error": str(ex), "type": str(type(ex))})


@csrf_exempt
def insert_sms_data(request):
    try:
        requesthandler(request)
        data = str(request.body)[2:-1]
        json_data = json.loads(data).get("ojson")
        sms_polling = SmsPolling(json_data)
        sms_polling.insert_sms_data()
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


def check_online_assets(request):
    r = requests.get("http://10.165.2.10:1810/api/getLive")
    offline_assets = []
    try:
        for asset in r.json():
                for key, value in asset.items():
                    if value == False:
                        assetnummer = key.capitalize()
                        asset = Asset.objects.select_related("laatste_data").get(assetnummer=assetnummer)
                        try:
                            tijdstip = asset.laatste_data.tijdstip.strftime("%d %b %Y, %H:%M")
                        except:
                            tijdstip = "Nooit"
                        if asset.pollbaar == True:
                            offline_assets.append(
                                {"assetnummer": asset.assetnummer, "tijdstip": tijdstip})
    except:
        pass
    return JsonResponse(offline_assets, safe=False)


def get_sensor_waarden_oud(request, assetnummer, veld):
    qs = AbsoluteData.objects.filter(assetnummer=assetnummer).order_by("tijdstip")
    data = list(qs.values(veld, "tijdstip"))
    response = []
    for item in data:
        response.append( [round(item["tijdstip"].timestamp()) * 1000, item[veld]])


    return JsonResponse(response, safe=False)

def get_sensor_waarden(request, assetnummer, veld):
    qs =  AbsoluteData.objects.filter(assetnummer=assetnummer, tijdstip__gte=datetime.date.today()).order_by("tijdstip")
    with open(f"./tram/templates/tram/data/{assetnummer}/{veld}.json") as json_file:
        data = json.load(json_file)
        data_vandaag = list(qs.values(veld, "tijdstip"))
        for item in data_vandaag:
            data.append([round((item["tijdstip"].timestamp()) * 1000), item[veld]])
    return JsonResponse(data, safe=False)

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
    qs = Asset.objects.exclude(ip_adres_logo=None).exclude(pollbaar=False)
    return JsonResponse(list(qs.values("assetnummer", "ip_adres_logo")) , safe=False)

def dashboard_omlopen(request):
    assets = Asset.objects.all()
    totale_omlopen = assets.aggregate(Sum("omloop_a"))["omloop_a__sum"] + assets.aggregate(Sum("omloop_b"))["omloop_b__sum"]
    asset_array = []

    def get_key(elem):
        return elem["y"]

    for asset in assets:
        asset_array.append(dict(name=asset.assetnummer, omlopen=asset.omloop_a+asset.omloop_b, y=((asset.omloop_a+asset.omloop_b) / totale_omlopen)*100))
    asset_array.sort(key=get_key, reverse=True) 

    return JsonResponse(dict(totale_omlopen=totale_omlopen, asset_array=asset_array))

def dashboard_omlopen_timerange(request, van_datum, tot_datum):
    start_datum = datetime.datetime.strptime(van_datum, "%d-%m-%Y")
    eind_datum = datetime.datetime.strptime(tot_datum, "%d-%m-%Y") + datetime.timedelta(days=1)
    assets = Asset.objects.all()
    totale_omlopen_qs = AbsoluteData.objects.filter(tijdstip__range=(start_datum, eind_datum))
    print(totale_omlopen_qs)
    som_a_omlopen = 0 if totale_omlopen_qs.aggregate(Sum("omloop_a_toegevoegd"))["omloop_a_toegevoegd__sum"] == None else totale_omlopen_qs.aggregate(Sum("omloop_a_toegevoegd"))["omloop_a_toegevoegd__sum"]
    som_b_omlopen = 0 if totale_omlopen_qs.aggregate(Sum("omloop_b_toegevoegd"))["omloop_b_toegevoegd__sum"] == None else totale_omlopen_qs.aggregate(Sum("omloop_b_toegevoegd"))["omloop_b_toegevoegd__sum"]

    totale_omlopen = som_a_omlopen + som_b_omlopen
    asset_array = []

    def get_key(elem):
        return elem["y"]

    for asset in assets:
        asset_omlopen_qs = AbsoluteData.objects.filter(assetnummer=asset, tijdstip__range=(start_datum, eind_datum))
        som_asset_a_omlopen = 0 if asset_omlopen_qs.aggregate(Sum("omloop_a_toegevoegd"))["omloop_a_toegevoegd__sum"] == None else asset_omlopen_qs.aggregate(Sum("omloop_a_toegevoegd"))["omloop_a_toegevoegd__sum"]
        som_asset_b_omlopen = 0 if asset_omlopen_qs.aggregate(Sum("omloop_b_toegevoegd"))["omloop_b_toegevoegd__sum"] == None else asset_omlopen_qs.aggregate(Sum("omloop_b_toegevoegd"))["omloop_b_toegevoegd__sum"]
        omlopen = som_asset_a_omlopen + som_asset_b_omlopen
        if omlopen == 0:
            continue
        asset_array.append(dict(name=asset.assetnummer, omlopen=0 if omlopen == None else omlopen, y=((asset.omloop_a+asset.omloop_b) / totale_omlopen)*100))
    asset_array.sort(key=get_key, reverse=True) 

    return JsonResponse(dict(totale_omlopen=totale_omlopen, asset_array=asset_array))

def dashboard_storingen(request, storing):
    tong_failure_synoniemen = ["Tong failure A+B", "Tongen failure A+B", "Tongen Failure A+B", "Tong failure A+B (H&K)", "Tongen failure A+B (ELL)"]

    if storing == "Tong failure A+B":
        qs = AbsoluteData.objects.filter(storing_beschrijving__overlap=tong_failure_synoniemen)
    else:   
        qs = AbsoluteData.objects.filter(storing_beschrijving__overlap=[storing])
    assets = Asset.objects.all()
    totale_storingen = qs.count()
    asset_array = []

    def get_key(elem):
        return elem["y"]

    for asset in assets:
        try:
            if storing == "Tong failure A+B":
                aantal = AbsoluteData.objects.filter(storing_beschrijving__overlap=tong_failure_synoniemen, assetnummer=asset).count()
            else:
                aantal = AbsoluteData.objects.filter(storing_beschrijving__overlap=[storing], assetnummer=asset).count()
            if aantal == 0:
                continue
            percentage = (aantal / totale_storingen)*100 if totale_storingen > 0 else 0

            asset_array.append(dict(name=asset.assetnummer, y= percentage))
        except ZeroDivisionError:
            continue
    asset_array.sort(key=get_key, reverse=True) 

    return JsonResponse(dict(totale_storingen=totale_storingen, asset_array=asset_array))

def dashboard_storingen_timerange(request, storing, van_datum, tot_datum):
    tong_failure_synoniemen = ["Tong failure A+B", "Tongen failure A+B", "Tongen Failure A+B", "Tong failure A+B (H&K)", "Tongen failure A+B (ELL)"]
    start_datum = datetime.datetime.strptime(van_datum, "%d-%m-%Y")
    eind_datum = datetime.datetime.strptime(tot_datum, "%d-%m-%Y") + datetime.timedelta(days=1)
    if storing == "Tong failure A+B":
        qs = AbsoluteData.objects.filter(storing_beschrijving__overlap=tong_failure_synoniemen,  tijdstip__range=(start_datum, eind_datum))
    else:   
        qs = AbsoluteData.objects.filter(storing_beschrijving__overlap=[storing],  tijdstip__range=(start_datum, eind_datum))
    assets = Asset.objects.all()
    totale_storingen = qs.count()
    asset_array = []

    def get_key(elem):
        return elem["y"]

    for asset in assets:
        if storing == "Tong failure A+B":
            aantal = AbsoluteData.objects.filter(storing_beschrijving__overlap=tong_failure_synoniemen, assetnummer=asset,  tijdstip__range=(start_datum, eind_datum)).count()
        else:
            aantal = AbsoluteData.objects.filter(storing_beschrijving__overlap=[storing], assetnummer=asset,  tijdstip__range=(start_datum, eind_datum)).count()
        if aantal == 0:
            continue
        percentage = (aantal / totale_storingen)*100  if totale_storingen > 0 else 0

        asset_array.append(dict(name=asset.assetnummer, y= percentage))
    asset_array.sort(key=get_key, reverse=True) 

    return JsonResponse(dict(totale_storingen=totale_storingen, asset_array=asset_array))

@csrf_exempt
def storing_filter(request):
    if request.method == 'POST':
        post_key = request.POST["key"]
        post_value = request.POST["value"]
        print(post_key)
        print(post_value)
        account_filter = request.user.account.storings_pagina_filter
        if post_value == "false":
            if post_key not in account_filter:
                account_filter.append(post_key)
        if post_value == "true":
            if post_key in account_filter:
                account_filter.remove(post_key)
        request.user.account.save()
        print(request.user.account.storings_pagina_filter)

        return HttpResponse(status=200)
    
    elif request.method == 'GET':
        return JsonResponse(json.dumps(request.user.account.storings_pagina_filter), safe=False)

