from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from ..models import *

def index(request):
    return render(request, "tram/index.html", {})

def storing_gezien(request, storing_id):
    storing = get_object_or_404(Storing, pk = storing_id)
    storing.gezien = True 
    storing.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def deactiveer_storing(request, storing_id):
    storing = get_object_or_404(Storing, pk = storing_id)
    storing.gezien = True
    storing.actief = False
    storing.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def sms_lijst(request):
    return render(request, "tram/sms.html")


