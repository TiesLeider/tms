from django.test import TestCase, Client
from django.urls import reverse
from tram.models import *
from tram.views import api
import json

#TMS API test
#Iedere test begint met een lege database!

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
    

    def tearDown(self):
        #Opruimen database
        AbsoluteData.objects.all().delete()
        Storing.objects.all().delete()
        Asset.objects.all().delete()
       

    def test_api_geslaagde_polling(self):
        #Test of de data wordt ingevoegd
        response = self.client.post(reverse("insert_logo_data"),
        json.dumps({"ojson": {"assetnummer":"w001","storing":0,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":1,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
        content_type="application/json"
        )
        self.assertEquals(str(response.json()), "{'response': True, 'error': None}") #Algoritme voltooid
        self.assertEquals(AbsoluteData.objects.all().count(), 1) #1 regel met data toegevoegd
        self.assertEquals(AbsoluteData.objects.first().assetnummer, self.asset) #Data is van dezelfde asset

    def test_api_polling_overgeslagen(self):
        #Test of de pollingen met gelijke data worden overgeslagen 
        response = self.client.post(reverse("insert_logo_data"),
        json.dumps({"ojson": {"assetnummer":"w001","storing":0,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":0,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
        content_type="application/json"
        )# <----- Wel want 1e polling
        
        response2 = self.client.post(reverse("insert_logo_data"),
        json.dumps({"ojson": {"assetnummer":"w001","storing":0,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":0,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
        content_type="application/json"
        )# <----- Niet want gelijk aan 1e polling
        
        self.assertEquals(AbsoluteData.objects.all().count(), 1)#Verwachting 1 regel aan data

        response3 = self.client.post(reverse("insert_logo_data"),
        json.dumps({"ojson": {"assetnummer":"w001","storing":0,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":1,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
        content_type="application/json"
        )# <----- Wel want verschilt tenopzichte van 1e polling

        self.assertEquals(AbsoluteData.objects.all().count(), 2)#Verwachting 2 regels aan data

    
    def test_api_storing_aangemaakt_no_timeout(self):
        #Test of de storing wordt aangemaakt (met een alarm zonder timeout)(Timeout houd in dat een alarm pas na een 2e alarm een storing word)
        response = self.client.post(reverse("insert_logo_data"),
            json.dumps({"ojson": {"assetnummer":"w001","storing":4,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":0,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
            content_type="application/json"
            )
        
        #Verwachtingen:
        self.assertEquals(AbsoluteData.objects.first().assetnummer, self.asset) #Eeste regel in de datatabel is van de asset
        self.assertIn("No Fail Save", AbsoluteData.objects.first().storing_beschrijving) #Eeste regel van de tabel met data bevat een melding van de storing
        self.assertEquals(Storing.objects.first().bericht, "No Fail Save") #Eerste regel in de storingstabel bevat een melding van de storing
        
    
    def test_api_storing_niet_aangemaakt_timeout(self):
        #Test of de storing niet wordt aangemaakt(met een alarm mét timeout)
        response = self.client.post(reverse("insert_logo_data"),
            json.dumps({"ojson": {"assetnummer":"w001","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":0,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
            content_type="application/json"
            )
        
        #Verwachtingen:
        self.assertIn("Tongen failure A+B", AbsoluteData.objects.first().storing_beschrijving) #Eeste regel van de datatabel bevat een melding van de storing
        self.assertEquals(Storing.objects.all().count(), 0) #Geen storingen aanwezig
    
    def test_api_storing_aangemaakt_timeout(self):
        #Test of de storing wel wordt aangemaakt(met een alarm mét timeout). 
        response = self.client.post(reverse("insert_logo_data"),
            json.dumps({"ojson": {"assetnummer":"w001","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":0,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
            content_type="application/json"
            )
        response2 = self.client.post(reverse("insert_logo_data"),
            json.dumps({"ojson": {"assetnummer":"w001","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":0,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
            content_type="application/json"
            )
        
        #Verwachtingen
        self.assertEquals(Storing.objects.first().assetnummer, self.asset) #eerste regel van de storingstabel is van de asset
        self.assertIn("Tongen failure A+B", AbsoluteData.objects.first().storing_beschrijving) #Eeste regel van de datatabel bevat een melding van de storing
        self.assertEquals(Storing.objects.first().bericht, "Tongen failure A+B") #Storing is aangemaakt met deze melding
        self.assertEquals(Storing.objects.first().som, 2) #Storing is inmiddels twee keer voor gekomen, want 2 meldingen
    
    def test_api_storing_geupdated(self):
        #Test of de data van dezelfde storing geupdate wordt
        response = self.client.post(reverse("insert_logo_data"),
            json.dumps({"ojson": {"assetnummer":"w001","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":0,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
            content_type="application/json"
            )#1e melding
        response2 = self.client.post(reverse("insert_logo_data"),
            json.dumps({"ojson": {"assetnummer":"w001","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":0,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
            content_type="application/json"
            )#2e melding

        self.assertEquals(Storing.objects.first().som, 2) #Storing 2x voorgekomen want 2 meldingen

        response3 = self.client.post(reverse("insert_logo_data"),
            json.dumps({"ojson": {"assetnummer":"w001","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":0,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
            content_type="application/json"
            )#3e melding
        self.assertEquals(Storing.objects.first().som, 3) #Storing 3x voorgekomen want 3 meldingen
    
    def test_api_weergeef_storing_na_negeren(self):
        # Test of de storing weer verschijnt na hem gezien gemeld te hebben
        response = self.client.post(reverse("insert_logo_data"),
            json.dumps({"ojson": {"assetnummer":"w001","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":0,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
            content_type="application/json"
            )
        response2 = self.client.post(reverse("insert_logo_data"),
            json.dumps({"ojson": {"assetnummer":"w001","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":0,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
            content_type="application/json"
        )
        S = Storing.objects.first()
        S.gezien = True #Gebruiker markeer storing als gezien
        S.save()

        #Verwachting:
        self.assertEquals(Storing.objects.first().gezien, True) #Storing moet gezien zijn

        response3 = self.client.post(reverse("insert_logo_data"),
            json.dumps({"ojson": {"assetnummer":"w001","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":0,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
            content_type="application/json"
            ) #Nieuwe melding

        #Verwachting:  
        self.assertEquals(Storing.objects.first().gezien, False)#Storing mag niet als gezien-gemeld zijn.
        

    def test_api_get_alle_storingen(self):
        #Haalt alle storingen op in de database.

        #Verwachting geen objecten, want geen data in database
        response = self.client.get(reverse("alle_actieve_storingen"))
        self.assertAlmostEquals(len(response.json()), 0)
    
        post = self.client.post(reverse("insert_logo_data"),
            json.dumps({"ojson": {"assetnummer":"w001","storing":4,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":0,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
            content_type="application/json"
        ) #<--------- Wel, want dit alarm kent geen timeout
        post = self.client.post(reverse("insert_logo_data"),
            json.dumps({"ojson": {"assetnummer":"w001","storing":8,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":0,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
            content_type="application/json"
        ) #<----------- Niet, geen storing want timeout
        response = self.client.get(reverse("alle_actieve_storingen"))

        #Verwachting is dus 1 object
        self.assertAlmostEquals(len(response.json()), 1)
    
    def test_api_get_sensorwaarden(self):
        #Haalt alle de data van 1 specifieke waarde
        post = self.client.post(reverse("insert_logo_data"),
            json.dumps({"ojson": {"assetnummer":"w001","storing":0,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":1,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
            content_type="application/json"
            )
        post2 = self.client.post(reverse("insert_logo_data"),
            json.dumps({"ojson": {"assetnummer":"w001","storing":0,"druk_b1":0,"druk_b2":0,"druk_a1":0,"druk_a2":0,"omloop_a":2,"omloop_b":0,"kracht_a":0,"kracht_b":0}}),
            content_type="application/json"
            )
        
        #Twee objecten in de database dus 2 opjecten zouden gereturned moeten worden.
        response = self.client.get(reverse("get_sensor_waarden_oud", args=["W001", "omloop_a"]))
        self.assertAlmostEquals(len(response.json()), 2)
    
    def test_api_get_ipnummers(self):
        #Returned alleen assets met een IP-adres EN die pollbaar zijn
        #W001 heeft geen IP-Adres dus <---- X
        self.asset = Asset.objects.create(assetnummer="W002", pollbaar=True, ip_adres_logo="1.1.1.1", configuratie=self.configuratie) #<---- V
        self.asset = Asset.objects.create(assetnummer="W003", pollbaar=True, ip_adres_logo=None, configuratie=self.configuratie) #<----- X
        self.asset = Asset.objects.create(assetnummer="W004", pollbaar=False, ip_adres_logo="1.1.1.1", configuratie=self.configuratie)#<---- X

        response = self.client.get(reverse("get_ipnummers"))
        self.assertAlmostEquals(len(response.json()), 1)

        self.asset = Asset.objects.create(assetnummer="W005", pollbaar=True, ip_adres_logo="1.1.1.1", configuratie=self.configuratie)#<---- V

        #Verwachting is nu dat er 2 objecten gereturned zullen worden
        response = self.client.get(reverse("get_ipnummers"))
        self.assertAlmostEquals(len(response.json()), 2)
