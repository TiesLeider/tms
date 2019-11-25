from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from ..models import *
import json

def requesthandler(request):
        if (request.body == "" or not request.body):
            return JsonResponse({"response": False, "error":  "POST inhoud niet aangekomen."})
        else:
            return request


@csrf_exempt
def insert_logo_data(request):
    try:
        def maak_nieuwe_storing(absulute_data, bericht):
            new_storing = Storing(
                assetnummer = absulute_data.assetnummer,
                gezien = False,
                actief = True,
                bericht = bericht,
                som = 1,
                score = 0,
                data = absulute_data
            )
            new_storing.score = new_storing.get_score()
            new_storing.save()

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

        #Wijzigingen in de assettabel:
        asset = Asset.objects.get(assetnummer=assetnummer)
        vorige_ad = AbsoluteData.objects.filter(assetnummer_id=assetnummer).order_by('-tijdstip').first()
        
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
            omloop_a = vorige_ad.omloop_a + record.omloop_a if (vorige_ad) else record.omloop_a,
            omloop_b = vorige_ad.omloop_b + record.omloop_b if (vorige_ad) else record.omloop_b,
        )
        asset = None
        vorige_ad = None
        ad.save()

        #Logica storing:

        #Er is een vorige polling geweest van deze asset
        if len(ad.storing_beschrijving) > 0:
            #Bij deze polling is een storing vastgelegd
            for sb in ad.storing_beschrijving:
                vorige_storing = Storing.objects.filter(assetnummer_id=ad.assetnummer.assetnummer, bericht=sb).order_by('-data__tijdstip').first()
                print(vorige_storing)
                if vorige_storing:
                    if (vorige_storing.actief == True) and (vorige_storing.gezien == False):
                        #De storing is niet gezien gemeld
                        vorige_storing.som += 1
                        vorige_storing.score = vorige_storing.get_score()
                        vorige_storing.data = ad
                    elif (vorige_storing.actief == True) and (vorige_storing.gezien == True):
                        #De storing is actief en gezien gemeld
                        vorige_storing.som += 1
                        vorige_storing.score = vorige_storing.get_score()
                        vorige_storing.gezien = False
                        vorige_storing.data = ad
                    elif (vorige_storing.actief == False):
                        #De storing is niet langer actief
                        if record.check_storing(sb) == True:
                            maak_nieuwe_storing(ad, sb)
                    vorige_storing.save()
                else:
                    #Er zijn geen storings-records gevonden van de vorige data
                    if record.check_storing(sb) == True:
                        maak_nieuwe_storing(ad, sb)
        else:
            #Er was geen storing bij deze polling
            pass
            
        return JsonResponse({"response": True, "error": None})
    except Exception as ex:
        return JsonResponse({"response": False, "error": str(ex)})

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