from django.shortcuts import render
from django.http import HttpResponse
from .models import LogoMelding

# Create your views here.

def index(request):
    context = LogoMelding.objects.all()

    return HttpResponse(context)
