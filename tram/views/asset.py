from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from ..models import *

def asset_index(request, assetnummer):
    asset = get_object_or_404(Asset, assetnummer=assetnummer)
    laatste_data = AbsoluteData.objects.filter(assetnummer=asset).order_by("-tijdstip")[:10]
    storingen = Storing.objects.filter(assetnummer=asset)[:10]
    return render(request, "tram/asset.html", {"asset": asset, "laatste_data":laatste_data, "storingen":storingen})