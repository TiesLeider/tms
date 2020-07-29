from django.test import TestCase, Client
from django.urls import reverse
from tram.models import *
from tram.views import asset
from django.contrib.auth.models import User


class TestApi(TestCase):
    def setUp(self):
        #Vullen van de database

        self.client = Client()
        self.urgentieniveau = Urgentieniveau.objects.create(niveau = 1, beschrijving = "Licht")
        self.configuratie = Configuratie.objects.create( 
            naam = "test_config", 
        )
        ConfiguratieElement.objects.create(inputnummer = 1, beschrijving = "Druk/Kracht (oil) point A", urgentieniveau = self.urgentieniveau, timeout = 24, configuratie = self.configuratie)
        ConfiguratieElement.objects.create(inputnummer = 2, beschrijving = "Druk/Kracht (force) point A", urgentieniveau = self.urgentieniveau, timeout = 24, configuratie = self.configuratie)
        ConfiguratieElement.objects.create(inputnummer = 3, beschrijving = "No Fail Save", urgentieniveau = self.urgentieniveau, timeout = 0, configuratie = self.configuratie)
        ConfiguratieElement.objects.create(inputnummer = 4, beschrijving = "Tongen failure A+B", urgentieniveau = self.urgentieniveau, timeout = 24, configuratie = self.configuratie)
        ConfiguratieElement.objects.create(inputnummer = 5, beschrijving = "Volgorde", urgentieniveau = self.urgentieniveau, timeout = 24, configuratie = self.configuratie)
        ConfiguratieElement.objects.create(inputnummer = 6, beschrijving = "WSA Defect", urgentieniveau = self.urgentieniveau, timeout = 24, configuratie = self.configuratie)
        ConfiguratieElement.objects.create(inputnummer = 7, beschrijving = "Druk/kracht (oil) point B", urgentieniveau = self.urgentieniveau, timeout = 24, configuratie = self.configuratie)
        ConfiguratieElement.objects.create(inputnummer = 8, beschrijving = "Druk/kracht (force) point B", urgentieniveau = self.urgentieniveau, timeout = 24, configuratie = self.configuratie)
        ConfiguratieElement.objects.create(inputnummer = 9, beschrijving = "Timeout L of R point A of Point B", urgentieniveau = self.urgentieniveau, timeout = 24, configuratie = self.configuratie)
        ConfiguratieElement.objects.create(inputnummer = 10, beschrijving = "Verzamelmelding deksels, water in bak", urgentieniveau = self.urgentieniveau, timeout = 24, configuratie = self.configuratie)
        ConfiguratieElement.objects.create(inputnummer = 11, beschrijving = "omloopteller bak A", urgentieniveau = self.urgentieniveau, timeout = 24, configuratie = self.configuratie)
        ConfiguratieElement.objects.create(inputnummer = 12, beschrijving = "omloopteller bak B", urgentieniveau = self.urgentieniveau, timeout = 24, configuratie = self.configuratie)
        self.asset = Asset.objects.create(assetnummer="W001", pollbaar=True, configuratie=self.configuratie)
    

    
    def test_toggle_asset_pollbaar(self):
        pass
        # User.objects.create_user(username='user', password='pass')
        # asset = asset.objects.get(assetnummer="W001")
        # self.assertAlmostEquals(asset.pollbaar, True)
        # self.client.login(username='user',password='pass')
    
