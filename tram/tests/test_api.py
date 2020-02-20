from django.test import TestCase
from tram.models import *

class TestApi(TestCase):

    def SetUp(self):
        asset = Asset.objects.create(assetnummer="W001")
        asset.configuratie = Configuratie.objects.get(naam="H&K-Standaard")
    
    

