import json
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ..models import *

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename="api.log", level=logging.INFO)

class Polling:

    def __init__(self, logo_data):
        self.record = logo_data
        self.assetnummer = self.record.assetnummer.assetnummer
        self.storing_beschrijving = self.record.get_storing_beschrijvingen()
        self.vorige_ad = self.get_laatste_asbolute_data()

    def insert_absolute_data(self):
        self.ad = AbsoluteData(
            assetnummer_id = self.record.assetnummer,
            storing_beschrijving = self.storing_beschrijving,
            druk_a1 = self.record.druk_a1,
            druk_a2 = self.record.druk_a2,
            druk_b1 = self.record.druk_b1,
            druk_b2 = self.record.druk_b2,
            kracht_a = self.record.kracht_a,
            kracht_b = self.record.kracht_b,
            omloop_a = self.vorige_ad.omloop_a + self.record.omloop_a if (self.vorige_ad) else self.record.omloop_a,
            omloop_b = self.vorige_ad.omloop_b + self.record.omloop_b if (self.vorige_ad) else self.record.omloop_b,
            )
        self.ad.save()


    def maak_nieuwe_storing(self, bericht, counter=1):
        logging.info("Nieuwe storing aangemaakt: %s: %s", self.assetnummer)
        new_storing = Storing(
            assetnummer_id = self.assetnummer,
            gezien = False,
            actief = True,
            bericht = bericht,
            laatste_data = self.ad,
            som = counter,
            score = 0,
        )
        new_storing.score = new_storing.get_score()
        new_storing.save()

    def get_laatste_asbolute_data(self):
        vorige_ad = AbsoluteData.objects.filter(assetnummer_id=self.assetnummer).latest()
        if (vorige_ad.assetnummer.assetnummer != self.assetnummer):
            logging.info("Verkeerde data opgehaald: %s. Verwacht was: %s", vorige_ad.assetnummer.assetnummer, self.assetnummer)
            for i in range(2, 21):
                vorige_ad = AbsoluteData.objects.filter(assetnummer_id=self.assetnummer).latest()
                if (vorige_ad.assetnummer.assetnummer == self.assetnummer):
                    logging.info("Data komt weer overeen met assetnummer: %s-%s", vorige_ad.assetnummer.assetnummer, self.assetnummer)
                    break
                if (vorige_ad.assetnummer.assetnummer != self.assetnummer):
                    logging.info("Poging %s: Verkeerde data opgehaald: %s. Verwacht was: %s", i, vorige_ad.assetnummer.assetnummer, self.assetnummer)
                if (i == 20):
                    logging.warning("Polling dropped: %s", self.assetnummer)
                    raise Exception(f"Fout bij het ophalen van data van asset {self.assetnummer}")

        return vorige_ad
        
        if not self.vorige_ad:
            logging.warning("Geen vorige data gevonden van assetnummer: %s", assetnummer)
            for i in range (1,6):
                logging.info("Poging %s: opnieuw data ophalen van asset: %s", i, assetnummer)
                self.vorige_ad = self.get_laatste_asbolute_data()
                if self.vorige_ad:
                    logging.info("Data gevonden van asset: %s!", assetnummer)
                    break
        
    def storing_algoritme(self):
        #Er is een vorige polling geweest van deze asset
        if len(self.storing_beschrijving) > 0:
            #Bij deze polling is een storing vastgelegd
            for sb in self.storing_beschrijving:
                #Check of dezelfde storing actief is
                #Zo ja: kijk huidige procedure
                #Zo niet: kijk of de deze beschrijving voorkwam in de afgelopen x (configuratie.timeout) uur of storing is voorgekomen
                    #Ja: maak nieuwe storing aan
                    #Nee: skip
                try:
                    vorige_storing = Storing.objects.filter(assetnummer=self.assetnummer, bericht=sb, actief=True).select_related("laatste_data").order_by('-laatste_data__tijdstip').first()
                    if vorige_storing:
                        if (vorige_storing.laatste_data.assetnummer.assetnummer != self.assetnummer):
                            logging.info("Verkeerde storing opgehaald: %s. Verwacht was: %s", vorige_storing.laatste_data.assetnummer.assetnummer, assetnummer)
                            for i in range(0, 21):
                                vorige_storing = Storing.objects.filter(assetnummer=self.assetnummer, bericht=sb).select_related("laatste_data").order_by('-laatste_data__tijdstip').first()
                                if (vorige_storing.laatste_data.assetnummer.assetnummer == self.assetnummer):
                                    logging.info("Storing komt weer overeen met assetnummer: %s-%s", vorige_storing.laatste_data.assetnummer.assetnummer, self.assetnummer)
                                    break
                                if (vorige_storing.laatste_data.assetnummer.assetnummer != self.assetnummer):
                                    logging.info("Poging %s: Verkeerde storing opgehaald: %s. Verwacht was: %s", i, vorige_storing.laatste_data.assetnummer.assetnummer, self.assetnummer)
                                if (i == 20):
                                    print(f"Polling dropped: {self.assetnummer}")
                                    raise Exception(f"Fout bij het ophalen van storing data van asset: {self.assetnummer}")
                except ObjectDoesNotExist:
                    vorige_storing = None
                if vorige_storing:
                    logging.info("assetnummer %s: vorige storingen: %s", self.assetnummer, Storing.objects.filter(assetnummer=self.assetnummer, bericht=sb, actief=True).select_related("laatste_data").order_by('-laatste_data__tijdstip'))
                    if (vorige_storing.gezien == False):
                        #De storing is niet gezien gemeld
                        vorige_storing.som += 1
                        vorige_storing.score = vorige_storing.get_score()
                        vorige_storing.laatste_data = self.ad
                    elif (vorige_storing.gezien == True):
                        #De storing is actief en gezien gemeld
                        vorige_storing.som += 1
                        vorige_storing.score = vorige_storing.get_score()
                        vorige_storing.gezien = False
                        vorige_storing.laatste_data = self.ad
                    vorige_storing.save()
                    logging.info("Storing met id: %s geupdate. assetnummer: %s", vorige_storing.id, vorige_storing.laatste_data.assetnummer.assetnummer)

                else:
                    #Check of storing voorkwam in de afgelopen x uur
                    for obj in self.ad.assetnummer.configuratie.config:
                        if obj.beschrijving == sb:
                            timeout = obj.timeout
                    
                    if timeout > 0:
                        recente_ads = AbsoluteData.objects.exclude(storing_beschrijving=[]).filter(assetnummer=self.ad.assetnummer, tijdstip__range=(datetime.datetime.now() - datetime.timedelta(hours=timeout), datetime.datetime.now()))
                        counter = 0
                        if recente_ads:
                            for rad in recente_ads:
                                if sb in rad.storing_beschrijving:
                                    counter += 1
                                    if counter > 1 and self.record.check_storing(sb) == True:
                                        logging.info("Nieuwe storing aangemaakt op basis van meerdere gelijke meldingen binnen timeout. asset: %s, storing: %s, aantal RADs: %s", self.ad.assetnummer.assetnummer, sb, recente_ads.count())
                                        self.maak_nieuwe_storing(sb, counter)
                                        break
                    else:
                        if self.record.check_storing(sb) == True:
                            logging.info("Nieuwe storing aangemaakt op basis van 0 timeout. asset: %s", self.ad.assetnummer.assetnummer)
                            self.maak_nieuwe_storing(sb)
