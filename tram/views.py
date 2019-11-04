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
        data = request.POST
        if (not data):
            return JsonResponse({"response": False, "error":  "Empty post"})
        print(data)
        record = LogoData(
            assetnummer_id = data.get("assetnummer"),
            storing = data.get("storing"),
            druk_a1 = data.get("druk_a1"),
            druk_a2 = data.get("druk_a2"),
            druk_b1 = data.get("druk_b1"),
            druk_b2 = data.get("druk_b2"),
            kracht_a = data.get("kracht_a"),
            kracht_b = data.get("kracht_b"),
            omloop_a = data.get("omloop_a"),
            omloop_b = data.get("omloop_b"),
            )  
        record.save()

        return JsonResponse({"response": True, "error": None})
    except Exception as ex:
        return JsonResponse({"response": False, "error": str(ex)})

