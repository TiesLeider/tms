from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from ..models import *

def asset_index(request, assetnummer):
    asset = get_object_or_404(Asset, assetnummer=assetnummer)
    storingen = Storing.objects.filter(assetnummer=asset)[:10]
    return render(request, "tram/asset.html", {"asset": asset,  "storingen":storingen})