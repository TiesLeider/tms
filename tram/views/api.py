from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ..models import *
import datetime
import json

def requesthandler(request):
        if (request.body == "" or not request.body):
            return JsonResponse({"response": False, "error":  "POST inhoud niet aangekomen."})
        else:
            return request


@csrf_exempt
def insert_logo_data(request):
    try:
        def maak_nieuwe_storing(asset, absulute_data, bericht):
            print("nieuwe_storing")
            new_storing = Storing(
                assetnummer = asset,
                gezien = False,
                actief = True,
                bericht = bericht,
                laatste_data = absulute_data,
                som = 1,
                score = 0,
            )
            new_storing.score = new_storing.get_score()
            new_storing.save()

        def get_vorige_ad(assetnummer):
            try:  
                vorige_ad, created = AssetLaatsteData.objects.get_or_create(assetnummer_id=assetnummer, defaults={"laatste_data": None})
                if created:
                    vorige_ad.laatste_data =  AbsoluteData.objects.filter(assetnummer_id=assetnummer).latest("tijdstip")
            except IntegrityError:
                for i in range(0, 10):
                    vorige_ad, created = AssetLaatsteData.objects.get(assetnummer_id=assetnummer)
                    if (assetnummer == vorige_ad.assetnummer.assetnummer):
                        return [vorige_ad, created]
                return None
        
            if (assetnummer != vorige_ad.assetnummer.assetnummer):
                for i in range(0, 10):
                    vorige_ad, created = AssetLaatsteData.objects.get_or_create(assetnummer_id=assetnummer, defaults={"laatste_data": None})
                    if (assetnummer == vorige_ad.assetnummer):
                        return [vorige_ad, created]
                return None
            
            return [vorige_ad, created]

        #Check of de requestdata ok is en manipuleer assetnummer:
        requesthandler(request)
        data = str(request.body)[2:-1]
        json_data = json.loads(data).get("ojson")
        assetnummer = json_data.get("assetnummer").upper() if json_data.get("assetnummer").startswith("w") else json_data.get("assetnummer")
        print(assetnummer)
        if len(assetnummer) > 4 and assetnummer.startswith("W"):
            assetnummer = assetnummer[1:]


        #Maak record Logodata:
        record = LogoData(
            assetnummer_id = assetnummer,
            storing = json_data.get("storing"),
            druk_a1 = json_data.get("druk_a1"),
            druk_a2 = json_data.get("druk_a2"),
            druk_b1 = json_data.get("druk_b1"),
            druk_b2 = json_data.get("druk_b2"),
            kracht_a = json_data.get("kracht_a"),
            kracht_b = json_data.get("kracht_b"),
            omloop_a = json_data.get("omloop_a"),
            omloop_b = json_data.get("omloop_b"),
            )
        record.save()

        
        # vorige_ad, created = get_vorige_ad(assetnummer)
        # if (vorige_ad == None):
        #     return JsonResponse({"response": True, "error": "Fout bij het ophalen van de data"})
        # created = False

        #Maak Absolutedata tabel
        ad = AbsoluteData(
            assetnummer_id = assetnummer,
            storing_beschrijving = record.get_storing_beschrijvingen() if (record.storing != 0) else [],
            druk_a1 = record.druk_a1,
            druk_a2 = record.druk_a2,
            druk_b1 = record.druk_b1,
            druk_b2 = record.druk_b2,
            kracht_a = record.kracht_a,
            kracht_b = record.kracht_b,
            omloop_a = record.omloop_a,
            omloop_b = record.omloop_b 
            # omloop_a = vorige_ad.laatste_data.omloop_a + record.omloop_a if (not created) else record.omloop_a,
            # omloop_b = vorige_ad.laatste_data.omloop_b + record.omloop_b if (not created) else record.omloop_b,
            )
        ad.save()
        # vorige_ad.laatste_data = ad
        # vorige_ad.save()


        Taak.objects.filter(project__id=Pid)

        #Er is een vorige polling geweest van deze asset
        if len(ad.storing_beschrijving) > 0:
            #Bij deze polling is een storing vastgelegd
            for sb in ad.storing_beschrijving:
                vorige_storing = Storing.objects.filter(assetnummer=ad.assetnummer, bericht=sb).select_related("laatste_data").order_by('-laatste_data__tijdstip').first()
                print(Storing.objects.filter(assetnummer=ad.assetnummer, bericht=sb).exists())
                if vorige_storing:
                    if (vorige_storing.actief == True) and (vorige_storing.gezien == False):
                        #De storing is niet gezien gemeld
                        vorige_storing.som += 1
                        vorige_storing.score = vorige_storing.get_score()
                        vorige_storing.laatste_data = ad
                    elif (vorige_storing.actief == True) and (vorige_storing.gezien == True):
                        #De storing is actief en gezien gemeld
                        vorige_storing.som += 1
                        vorige_storing.score = vorige_storing.get_score()
                        vorige_storing.gezien = False
                        vorige_storing.laatste_data = ad
                    elif (vorige_storing.actief == False):
                        #De storing is niet langer actief
                        if record.check_storing(sb) == True:
                            maak_nieuwe_storing(ad.assetnummer, ad, sb)
                    vorige_storing.save()
                else:
                    #Er zijn geen storings-records gevonden van de vorige data
                    if record.check_storing(sb) == True:
                        maak_nieuwe_storing(ad.assetnummer, ad, sb)
        else:
            #Er was geen storing bij deze polling
            pass
        return JsonResponse({"response": True, "error": None})
    except Exception as ex:
        return JsonResponse({"response": False, "error": str(ex), "type": str(type(ex))})

@csrf_exempt
def insert_logo_online(request):
    try:
        requesthandler(request)
        data = str(request.body)[2:-1]
        json_data = json.loads(data).get("ojson")
        print(json_data)
        assetnummer = json_data.get("assetnummer").upper() if (json_data.get("assetnummer").startswith("w")) else json_data.get("assetnummer")
        asset = Asset.objects.get(assetnummer=assetnummer)
        asset.logo_online = False
        asset.disconnections += 1
        asset.save()

        return JsonResponse({"response": True, "error": None})
    except Exception as ex:
        return JsonResponse({"response": False, "error": str(ex)})

def get_omlopen(request, assetnummer, van_datum, tot_datum):
    start_datum = datetime.datetime.strptime(van_datum, "%d-%m-%Y")
    eind_datum = datetime.datetime.strptime(tot_datum, "%d-%m-%Y") + datetime.timedelta(days=1)
    ad_qs = AbsoluteData.objects.filter(assetnummer=assetnummer, tijdstip__range=(start_datum, eind_datum))
    data = list(ad_qs.values("tijdstip", "omloop_a", "omloop_b"))
    response = {
        "labels": list(ad_qs.values_list("tijdstip", flat=True)),
        "data": [
                list(ad_qs.values_list("omloop_a", flat=True)),
                list(ad_qs.values_list("omloop_b", flat=True))
        ]
        }
    return JsonResponse(response, safe=False)

def get_actieve_storingen(request):
    storingen_qs = Storing.objects.filter(actief=True, gezien=False).order_by("-laatste_data__tijdstip")
    data = list(storingen_qs.values("id", "laatste_data__assetnummer__assetnummer", "bericht", "som", "score", "laatste_data__omloop_a", "laatste_data__omloop_b", "laatste_data__tijdstip"))
    for item in data:
        item["laatste_data__tijdstip"] = item["laatste_data__tijdstip"].strftime("%d %b %Y, %H:%M")
    return JsonResponse(data, safe=False)