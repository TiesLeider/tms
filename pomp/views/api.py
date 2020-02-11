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

def requesthandler(request):
        if (request.body == "" or not request.body):
            return JsonResponse({"response": False, "error":  "POST inhoud niet aangekomen."})
        else:
            return request

@csrf_exempt
def insert_data(request):
    try:
        def maak_nieuwe_storing(asset, bericht):
            nieuwe_storing = Storing(
                asset = asset,
                beschrijving = bericht,
            )
            nieuwe_storing.save()

        requesthandler(request)
        data = str(request.body)[2:-1]
        json_data = json.loads(data).get("ojson")
        asset, created = Asset.objects.get_or_create(assetnummer=json_data.get("assetnummer"),
        defaults = {"configuratie": Configuratie.objects.get(naam="Standaard")})
        record = Data(
            asset  = asset,
            storing = json_data.get("storing"),
            niveau = json_data.get("niveau")
        )

        record.save()
        if record.storing > 0:
            for s in record.get_storing_beschrijvingen():
                maak_nieuwe_storing(record.asset, s)
        return JsonResponse({"response": True, "error": None})
    except Exception as ex:
        traceback.print_exc()
        return JsonResponse({"response": False, "error": str(ex), "type": str(type(ex))})

def get_storingen(request):
    storingen = Storing.objects.all()
    response = list(storingen.values("asset__assetnummer", "beschrijving", "tijdstip"))
    return JsonResponse(response, safe=False)

def get_data(request):
    data = Data.objects.all()
    response = list(data.values("asset__assetnummer", "storing", "niveau", "tijdstip"))
    return JsonResponse(response, safe=False)

