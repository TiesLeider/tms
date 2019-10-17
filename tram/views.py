from django.shortcuts import render
from django.http import HttpResponse
from .models import LogoMelding

# Create your views here.

def index(request):
    context = LogoMelding.objects.all()
    list = []

    for item in context:
        list.append(item.assetnummer)
    return HttpResponse(list)
