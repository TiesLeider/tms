import json
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ..models import *
import datetime
from django.db.models import Sum

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', filename="api.log", level=logging.INFO)


class LogoPolling:

    def __init__(self, logo_data):
        self.record = logo_data
        self.assetnummer = self.record.assetnummer.assetnummer
        self.storing_beschrijving = self.record.get_storing_beschrijvingen()
        self.vorige_ad = self.get_laatste_asbolute_data()

    def insert_absolute_data(self):
        self.ad = AbsoluteData(
            assetnummer_id=self.record.assetnummer,
            storing_beschrijving=self.storing_beschrijving,
            druk_a1=self.record.druk_a1,
            druk_a2=self.record.druk_a2,
            druk_b1=self.record.druk_b1,
            druk_b2=self.record.druk_b2,
            kracht_a=self.record.kracht_a,
            kracht_b=self.record.kracht_b,
            omloop_a=self.vorige_ad.omloop_a +
            self.record.omloop_a if (self.vorige_ad) else self.record.omloop_a,
            omloop_b=self.vorige_ad.omloop_b +
            self.record.omloop_b if (self.vorige_ad) else self.record.omloop_b,
        )
        self.ad.save()

    def maak_nieuwe_storing(self, bericht, counter=1):
        logging.info(
            f"{self.assetnummer}: Nieuwe storing aangemaakt:  {bericht}")
        new_storing = Storing(
            assetnummer_id=self.assetnummer,
            gezien=False,
            actief=True,
            bericht=bericht,
            laatste_data=self.ad,
            som=counter,
            score=0,
        )
        new_storing.score = new_storing.get_score()
        new_storing.save()

    def get_laatste_asbolute_data(self):
        try:
            vorige_ad = AbsoluteData.objects.filter(
                assetnummer_id=self.assetnummer).latest()
        except ObjectDoesNotExist:
            vorige_ad = None
        return vorige_ad

    def storing_algoritme(self):
        # Er is een vorige polling geweest van deze asset
        if len(self.storing_beschrijving) > 0:
            # Bij deze polling is een storing vastgelegd
            for sb in self.storing_beschrijving:
                # Check of dezelfde storing actief is
                # Zo ja: kijk huidige procedure
                # Zo niet: kijk of de deze beschrijving voorkwam in de afgelopen x (configuratie.timeout) uur of storing is voorgekomen
                    # Ja: maak nieuwe storing aan
                    # Nee: skip
                try:
                    vorige_storingen = Storing.objects.filter(assetnummer=self.assetnummer, bericht=sb, actief=True).select_related("laatste_data").order_by('-laatste_data__tijdstip')
                    vorige_storing = vorige_storingen.first()
                except ObjectDoesNotExist:
                    vorige_storing = None
                if vorige_storing:
                    if vorige_storingen.count() > 1:
                        print(vorige_storing)
                        vorige_storing.som = vorige_storingen.aggregate(Sum("som"))["som__sum"]
                        logging.info(f'{self.assetnummer}: aggregate: {vorige_storingen.aggregate(Sum("som"))["som__sum"]}')
                        for s in vorige_storingen.exclude(id=vorige_storing.id):
                            s.delete()

                    logging.info(f"{self.assetnummer}: vorige storingen: {vorige_storingen}")
                    if (vorige_storing.gezien == False):
                        # De storing is niet gezien gemeld
                        vorige_storing.som += 1
                        vorige_storing.score = vorige_storing.get_score()
                        vorige_storing.laatste_data = self.ad
                    elif (vorige_storing.gezien == True):
                        # De storing is actief en gezien gemeld
                        vorige_storing.som += 1
                        vorige_storing.score = vorige_storing.get_score()
                        vorige_storing.gezien = False
                        vorige_storing.laatste_data = self.ad
                    vorige_storing.save()
                    logging.info(f"{self.assetnummer}: Storing met id: {vorige_storing.id} geupdate.")

                else:
                    # Check of storing voorkwam in de afgelopen x uur
                    for obj in self.ad.assetnummer.configuratie.config:
                        if obj.beschrijving == sb:
                            timeout = obj.timeout

                    if timeout > 0:
                        recente_ads = AbsoluteData.objects.exclude(storing_beschrijving=[]).filter(assetnummer=self.ad.assetnummer, tijdstip__range=(
                            datetime.datetime.now() - datetime.timedelta(hours=timeout), datetime.datetime.now()))
                        counter = 0
                        if recente_ads:
                            for rad in recente_ads:
                                if sb in rad.storing_beschrijving:
                                    counter += 1
                                    if counter > 1 and self.record.check_storing(sb) == True:
                                        logging.info(f"{self.assetnummer}: Nieuwe storing aangemaakt op basis van meerdere gelijke meldingen binnen timeout. storing: {sb}, aantal RADs: {recente_ads.count()}")
                                        self.maak_nieuwe_storing(sb, counter)
                                        break
                    else:
                        if self.record.check_storing(sb) == True:
                            logging.info(
                                f"{self.assetnummer}: Nieuwe storing aangemaakt op basis van 0 timeout.")
                            self.maak_nieuwe_storing(sb)

class SmsPolling:
    
    def __init__(self, json_data):
        self.ontvangen = datetime.datetime.strptime(json_data.get("received"), "%Y-%m-%d %H:%M:%S")
        self.modem = json_data.get("modem")
        self.telnummer = json_data.get("from")
        self.storing = json_data.get("omschrijving")
        self.smsc = json_data.get("smsc")
        self.udh = True if (json_data.get("udh") == "true") else False
        self.inputnummer = int(json_data.get("input"))
        self.status = json_data.get("status")
        self.alphabet = json_data.get("alphabet")
        self.sent = datetime.datetime.strptime(json_data.get("sent"), "%Y-%m-%d %H:%M:%S")
        self.sim = json_data.get("sim")
        self.asset = json_data.get("wissel")

    def insert_sms_data(self):
        record = SmsData(
            ontvangen = self.ontvangen,
            modem = self.modem,
            telnummer = self.telnummer,
            storing = self.storing,
            smsc = self.smsc,
            udh = self.udh,
            inputnummer = self.inputnummer,
            status = self.status,
            alphabet = self.alphabet,
            sent = self.sent,
            sim = self.sim,
            asset = self.asset
        )
        record.save()
