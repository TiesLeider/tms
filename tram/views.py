from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from pprint import pprint

# Create your views here.

def index(request):
    return render(request, "tram/index.html", {"meldingen": LogoData.objects.exclude(storing=0).order_by('-tijdstip')})

@csrf_exempt
def insert_logo_data(request):
    try:

        if (request.body == "" or not request.body):
            return JsonResponse({"response": False, "error":  "Empty post"})
        data = str(request.body)[2:-1]
        json_data = json.loads(data).get("ojson")
        print(json_data)
        record = LogoData(
            assetnummer_id = json_data.get("assetnummer"),
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
        
        asset = Asset().objects.get(assetnummer=json_data.get("assetnummer"))
        asset.logo_online = True
        asset.disconnections = 0
        asset.laatste_storing = json_data.get("storing")
        asset.save()


        return JsonResponse({"response": True, "error": None})
    except Exception as ex:
        return JsonResponse({"response": False, "error": str(ex), "json":json_data})

@csrf_exempt
def insert_logo_online(request):
    try:
        if (request.body == "" or not request.body):
            return JsonResponse({"response": False, "error":  "Empty post"})
        data = str(request.body)[2:-1]
        json_data = json.loads(data).get("ojson")
        print(json_data)
        
        asset = Asset().objects.get(assetnummer=json_data.get("assetnummer"))
        asset.logo_online = False
        asset.disconnections += 1
        asset.laatste_storing = json_data.get("storing")
        asset.save()

        return JsonResponse({"response": True, "error": None})
    except Exception as ex:
        return JsonResponse({"response": False, "error": str(ex)})


