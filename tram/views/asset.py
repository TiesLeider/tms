from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from ..models import *
from django.db.models import Sum, Avg


def asset_index(request, assetnummer):
    asset = get_object_or_404(Asset, assetnummer=assetnummer)
    laatste_polling = AbsoluteData.objects.filter(assetnummer=asset).latest("tijdstip")
    laatste_data = AbsoluteData.objects.filter(assetnummer=asset).exclude(storing_beschrijving=[]).order_by("-tijdstip")[:15]

    return render(request, "tram/asset.html", {"asset": asset, "laatste_data":laatste_data, "laatste_polling": laatste_polling})

def reset_teller_standen(request, assetnummer):
    asset = get_object_or_404(Asset, assetnummer=assetnummer)
    laatste_data = AbsoluteData.objects.filter(assetnummer=asset).latest("tijdstip")
    laatste_data.omloop_a = 0
    laatste_data.omloop_b = 0
    laatste_data.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def reset_teller_alle(request):
    for asset in Asset.objects.all():
        try:
            laatste_data = AbsoluteData.objects.filter(assetnummer=asset).latest("tijdstip")
            laatste_data.omloop_a = 0
            laatste_data.omloop_b = 0
            laatste_data.save()
        except:
            pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def corrigeer_omlopen(request, assetnummer):
    som = AbsoluteData.objects.filter(assetnummer=assetnummer, tijdstip__range=(datetime.datetime(2020, 3, 11), datetime.datetime.now())).aggregate(Sum("omloop_a_toegevoegd"))
    ad = AbsoluteData.objects.filter(assetnummer=assetnummer).latest()
    ad.omloop_a = som["omloop_a__sum"]
    ad.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def asset_chart(request, assetnummer):
    asset = get_object_or_404(Asset, assetnummer=assetnummer)
    return render(request, "tram/chart.html", {"asset": asset})

def asset_analyse(request, assetnummer, veld):
    asset = get_object_or_404(Asset, assetnummer=assetnummer)
    return render(request, "tram/highstock.html", {"asset": asset, "veld" : veld})