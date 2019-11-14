from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json

# Create your views here.


def index(request):
    return render(request, "tram/index.html", {"storingen": Storing.objects.filter(actief=True, gezien=False).order_by('-som')})
    # return render(request, "tram/index.html", {"storingen": AbsoluteData.objects.exclude(storing_beschrijving=[]).order_by("-tijdstip")})

def storing_gezien(request, storing_id):
    storing = get_object_or_404(Storing, pk = storing_id)
    storing.gezien = True
    storing.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def deactiveer_storing(request, storing_id):
    storing = get_object_or_404(Storing, pk = storing_id)
    storing.gezien = True
    storing.actief = False
    storing.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def requesthandler(request):
        if (request.body == "" or not request.body):
            return JsonResponse({"response": False, "error":  "POST inhoud niet aangekomen."})
        else:
            return request
        
@csrf_exempt
def insert_logo_data(request):
    try:
        requesthandler(request)
        data = str(request.body)[2:-1]
        json_data = json.loads(data).get("ojson")
        assetnummer = json_data.get("assetnummer").upper() if json_data.get("assetnummer").startswith("w") else json_data.get("assetnummer")
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
        if assetnummer == "W2641" or assetnummer == "W2642":
            assetnummer = assetnummer[1:]
        
        asset = Asset.objects.get(assetnummer=assetnummer)
        asset.logo_online = False
        asset.disconnections += 1
        asset.save()

        return JsonResponse({"response": True, "error": None})
    except Exception as ex:
        return JsonResponse({"response": False, "error": str(ex)})


