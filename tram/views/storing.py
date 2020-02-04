from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from ..models import *

def index(request):
    return render(request, "tram/index.html", {"storingen": Storing.objects.filter(actief=True, gezien=False).select_related("laatste_data").order_by("-laatste_data__tijdstip")[:30]})

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

def sms_lijst(request):
    return render(request, "tram/sms.html")


