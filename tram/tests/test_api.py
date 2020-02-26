from django.test import TestCase, Client
from django.urls import reverse
from tram.models import *
from tram.views import api
import json



class TestApi(TestCase):
    def SetUp(self):
        self.client = Client()
        self.asset = Asset.objects.create(assetnummer="W001")
        self.urgentieniveau = Urgentieniveau.objects.create(niveau = 1, beschrijving = "Licht")
        self.configuratie = Configuratie.objects.create( 
            naam = "test_config", 
            config = [
                ConfiguratieElement(inputnummer = 1, beschrijving = "Druk/Kracht (oil) point A", urgentieniveau = self.urgentieniveau, timeout = 24),
                ConfiguratieElement(inputnummer = 2, beschrijving = "Druk/Kracht (force) point A", urgentieniveau = self.urgentieniveau, timeout = 24),
                ConfiguratieElement(inputnummer = 3, beschrijving = "No Fail Save", urgentieniveau = self.urgentieniveau, timeout = 24),
                ConfiguratieElement(inputnummer = 4, beschrijving = "Tongen failure A+B", urgentieniveau = self.urgentieniveau, timeout = 24),
                ConfiguratieElement(inputnummer = 5, beschrijving = "Volgorde", urgentieniveau = self.urgentieniveau, timeout = 24),
                ConfiguratieElement(inputnummer = 6, beschrijving = "WSA Defect", urgentieniveau = self.urgentieniveau, timeout = 24),
                ConfiguratieElement(inputnummer = 7, beschrijving = "Druk/kracht (oil) point B", urgentieniveau = self.urgentieniveau, timeout = 24),
                ConfiguratieElement(inputnummer = 8, beschrijving = "Druk/kracht (force) point B", urgentieniveau = self.urgentieniveau, timeout = 24),
                ConfiguratieElement(inputnummer = 9, beschrijving = "Timeout L of R point A of Point B", urgentieniveau = self.urgentieniveau, timeout = 24),
                ConfiguratieElement(inputnummer = 10, beschrijving = "Verzamelmelding deksels, water in bak", urgentieniveau = self.urgentieniveau, timeout = 24),
                ConfiguratieElement(inputnummer = 11, beschrijving = "omloopteller bak A", urgentieniveau = self.urgentieniveau, timeout = 24),
                ConfiguratieElement(inputnummer = 12, beschrijving = "omloopteller bak B", urgentieniveau = self.urgentieniveau, timeout = 24),
            ])
        self.asset.configuratie = self.configuratie
    
    def test_api(self):
        pass
        # response = self.client.post(reverse("insert_logo_online"),
        # json.dumps({"ojson": {
        #     "assetnummer":"W001",
        #     "storing":0,
        #     "druk_b1":0,
        #     "druk_b2":0,
        #     "druk_a1":0,
        #     "druk_a2":0,
        #     "omloop_a":0,
        #     "omloop_b":1,
        #     "kracht_a":0,
        #     "kracht_b":0
        #     }
        # })
        # )

        # self.assertEquals(response.json(), '{"response": True, "error": None}')
