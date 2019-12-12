from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ..models import *
import traceback
import datetime
import json
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename="api.log", level=logging.INFO)

def requesthandler(request):
        if (request.body == "" or not request.body):
            return JsonResponse({"response": False, "error":  "POST inhoud niet aangekomen."})
        else:
            return request


@csrf_exempt
def insert_logo_data(request):
    try:
        def maak_nieuwe_storing(asset, absulute_data, bericht, counter=1):
            logging.info("Nieuwe storing aangemaakt: %s: %s", asset, bericht)
            new_storing = Storing(
                assetnummer = asset,
                gezien = False,
                actief = True,
                bericht = bericht,
                laatste_data = absulute_data,
                som = counter,
                score = 0,
            )
            new_storing.score = new_storing.get_score()
            new_storing.save()


        #Check of de requestdata ok is en manipuleer assetnummer:
        requesthandler(request)
        data = str(request.body)[2:-1]
        json_data = json.loads(data).get("ojson")
        assetnummer = json_data.get("assetnummer").upper() if json_data.get("assetnummer").startswith("w") else json_data.get("assetnummer")
        if len(assetnummer) > 4 and assetnummer.startswith("W"):
            assetnummer = assetnummer[1:]
        
        try:
            vorige_ad = AbsoluteData.objects.filter(assetnummer_id=assetnummer).latest()
            if (vorige_ad.assetnummer.assetnummer != assetnummer):
                logging.info("Verkeerde data opgehaald: %s. Verwacht was: %s", vorige_ad.assetnummer.assetnummer, assetnummer)
                for i in range(2, 21):
                    vorige_ad = AbsoluteData.objects.filter(assetnummer_id=assetnummer).latest()
                    if (vorige_ad.assetnummer.assetnummer == assetnummer):
                        logging.info("Data komt weer overeen met assetnummer: %s-%s", vorige_ad.assetnummer.assetnummer, assetnummer)
                        break
                    if (vorige_ad.assetnummer.assetnummer != assetnummer):
                        logging.info("Poging %s: Verkeerde data opgehaald: %s. Verwacht was: %s", i, vorige_ad.assetnummer.assetnummer, assetnummer)
                    if (i == 20):
                        logging.warning("Polling dropped: %s", assetnummer)
                        return JsonResponse({"response": False, "error": "Fout bij het ophalen van de data"})
        except ObjectDoesNotExist:
            vorige_ad = None


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


        #Maak Absolutedata tabel
        if not vorige_ad:
            logging.warning("Geen vorige data gevonden van assetnummer: %s", assetnummer)
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
        ad.save()
        # vorige_ad.laatste_data = ad
        # vorige_ad.save()


        #Er is een vorige polling geweest van deze asset
        if len(ad.storing_beschrijving) > 0:
            #Bij deze polling is een storing vastgelegd
            for sb in ad.storing_beschrijving:
                #Check of dezelfde storing actief is
                #Zo ja: kijk huidige procedure
                #Zo niet: kijk of de deze beschrijving voorkwam in de afgelopen x (configuratie.timeout) uur of storing is voorgekomen
                    #Ja: maak nieuwe storing aan
                    #Nee: skip
                try:
                    vorige_storing = Storing.objects.filter(assetnummer=ad.assetnummer, bericht=sb, actief=True).select_related("laatste_data").order_by('-laatste_data__tijdstip').first()
                    if vorige_storing:
                        if (vorige_storing.laatste_data.assetnummer.assetnummer != assetnummer):
                            logging.info("Verkeerde storing opgehaald: %s. Verwacht was: %s", vorige_storing.laatste_data.assetnummer.assetnummer, assetnummer)
                            for i in range(0, 21):
                                vorige_storing = Storing.objects.filter(assetnummer=ad.assetnummer, bericht=sb).select_related("laatste_data").order_by('-laatste_data__tijdstip').first()
                                if (vorige_storing.laatste_data.assetnummer.assetnummer == assetnummer):
                                    logging.info("Storing komt weer overeen met assetnummer: %s-%s", vorige_storing.laatste_data.assetnummer.assetnummer, assetnummer)
                                    break
                                if (vorige_storing.laatste_data.assetnummer.assetnummer != assetnummer):
                                     logging.info("Poging %s: Verkeerde storing opgehaald: %s. Verwacht was: %s", i, vorige_storing.laatste_data.assetnummer.assetnummer, assetnummer)
                                if (i == 20):
                                    print(f"Polling dropped: {assetnummer}")
                                    return JsonResponse({"response": False, "error": "Fout bij het ophalen van de storing data"})
                except ObjectDoesNotExist:
                    vorige_storing = None
                if vorige_storing:
                    if (vorige_storing.gezien == False):
                        #De storing is niet gezien gemeld
                        vorige_storing.som += 1
                        vorige_storing.score = vorige_storing.get_score()
                        vorige_storing.laatste_data = ad
                    elif (vorige_storing.gezien == True):
                        #De storing is actief en gezien gemeld
                        vorige_storing.som += 1
                        vorige_storing.score = vorige_storing.get_score()
                        vorige_storing.gezien = False
                        vorige_storing.laatste_data = ad
                    logging.info("Storing met id: %s geupdate. assetnummer: %s", vorige_storing.id, vorige_storing.laatste_data.assetnummer.assetnummer)
                    vorige_storing.save()
                else:
                    #Check of storing voorkwam in de afgelopen x uur
                    for obj in ad.assetnummer.configuratie.config:
                        if obj.beschrijving == sb:
                            timeout = obj.timeout
                    
                    if timeout > 0:
                        recente_ads = AbsoluteData.objects.exclude(storing_beschrijving=[]).filter(assetnummer=ad.assetnummer, tijdstip__range=(datetime.datetime.now() - datetime.timedelta(hours=timeout), datetime.datetime.now()))
                        counter = 0
                        if recente_ads:
                            for rad in recente_ads:
                                if sb in rad.storing_beschrijving:
                                    counter += 1
                                    if counter > 1 and record.check_storing(sb) == True:
                                        logging.info("Nieuwe storing aangemaakt op basis van meerdere gelijke meldingen binnen timeout. asset: %s, storing: %s, aantal RADs: %s", ad.assetnummer.assetnummer, sb, recente_ads.count())
                                        maak_nieuwe_storing(ad.assetnummer, ad, sb, counter)
                                        break
                    else:
                        if record.check_storing(sb) == True:
                            logging.info("Nieuwe storing aangemaakt op basis van 0 timeout. asset: %s", ad.assetnummer.assetnummer)
                            maak_nieuwe_storing(ad.assetnummer, ad, sb)
        else:
            #Er was geen storing bij deze polling
            pass
        return JsonResponse({"response": True, "error": None})
    except Exception as ex:
        traceback.print_exc()
        return JsonResponse({"response": False, "error": str(ex), "type": str(type(ex))})

@csrf_exempt
def insert_logo_online(request):
    try:
        requesthandler(request)
        data = str(request.body)[2:-1]
        json_data = json.loads(data).get("ojson")
        assetnummer = json_data.get("assetnummer").upper() if (json_data.get("assetnummer").startswith("w")) else json_data.get("assetnummer")
        asset = Asset.objects.get(assetnummer=assetnummer)
        asset.logo_online = False
        asset.disconnections += 1
        asset.save()

        return JsonResponse({"response": True, "error": None})
    except Exception as ex:
        return JsonResponse({"response": False, "error": str(ex)})

def get_omlopen_totaal(request, assetnummer, van_datum, tot_datum):
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

def get_omlopen_freq(request, assetnummer, van_datum, tot_datum):
    start_datum = datetime.datetime.strptime(van_datum, "%d-%m-%Y")
    eind_datum = datetime.datetime.strptime(tot_datum, "%d-%m-%Y") + datetime.timedelta(days=1)
    ld_qs = LogoData.objects.filter(assetnummer=assetnummer, tijdstip__range=(start_datum, eind_datum))
    data = list(ld_qs.values("tijdstip", "omloop_a", "omloop_b"))
    response = {
        "labels": list(ld_qs.values_list("tijdstip", flat=True)),
        "data": [
                list(ld_qs.values_list("omloop_a", flat=True)),
                list(ld_qs.values_list("omloop_b", flat=True))
        ]
        }
    return JsonResponse(response, safe=False)

def get_actieve_storingen(request):
    storingen_qs = Storing.objects.filter(actief=True, gezien=False).order_by("-laatste_data__tijdstip")
    data = list(storingen_qs.values("id", "laatste_data__assetnummer__assetnummer", "bericht", "som", "score", "laatste_data__omloop_a", "laatste_data__omloop_b", "laatste_data__tijdstip"))
    for item in data:
        item["laatste_data__tijdstip"] = item["laatste_data__tijdstip"].strftime("%d %b %Y, %H:%M")
    return JsonResponse(data, safe=False)

def index_form(request):
    if request.method == "POST":
        data = str(request.body)[2:-1]
        json_data = json.loads(data).get("geselecteerde_storingen")
        
        for sid in json_data:
                storing = get_object_or_404(Storing, pk = sid)
                storing.gezien = True
                if json.loads(data).get("method") == "herstellen":
                    storing.actief = False
                storing.save()

        return HttpResponse(request.POST.dict())
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))