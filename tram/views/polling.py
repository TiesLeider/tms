import json
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from ..models import *
import datetime
from django.db.models import Sum

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', filename="api.log", level=logging.INFO)

class LogoData():
    
    def __init__(self, json_data, asset):
        self.assetnummer = asset
        self.storing = json_data.get("storing")
        self.druk_a1 = json_data.get("druk_a1")
        self.druk_a2 = json_data.get("druk_a2")
        self.druk_b1 = json_data.get("druk_b1")
        self.druk_b2 = json_data.get("druk_b2")
        self.kracht_a = json_data.get("kracht_a")
        self.kracht_b = json_data.get("kracht_b")
        self.omloop_a = json_data.get("omloop_a")
        self.omloop_b = json_data.get("omloop_b")

    class Meta:
        verbose_name_plural = "logo data"
        get_latest_by = "tijdstip"

    def get_bin_waarden(self):
    #Het omzetten van de hex/int waarde naar binaire waarden
        inputs = []
        for pin in bin(self.storing)[2:]:
            inputs.append(int(pin))
        inputs.reverse()
        return inputs

    def get_hoge_inputs(self):
    #Gebruikt de binaire waarden om te bepalen welke waarden hoog zijn.
        hoge_inputs = []
        for idx, val in enumerate(self.get_bin_waarden()):
            if val != 0:
                hoge_inputs.append(idx+1)
        return hoge_inputs

    def get_storing_beschrijvingen(self):
        beschrijvingen = []
        for hoge_input in self.get_hoge_inputs():
            beschrijvingen.append(ConfiguratieElement.objects.get(configuratie=self.assetnummer.configuratie, inputnummer=hoge_input).beschrijving)
        return beschrijvingen

    def get_storings_score(self):
        score = 0
        for hoge_input in self.get_hoge_inputs():
            score += ConfiguratieElement.objects.get(Configuratie=self.assetnummer.configuratie, inputnummer=hoge_input).urgentiniveau.niveau
        return score
    
    def check_storing(self, storing_beschrijving):
        return storing_beschrijving in self.get_storing_beschrijvingen()

class LogoPolling:

    def __init__(self, logo_data, asset):
        self.record = logo_data
        self.asset = asset
        self.assetnummer = self.asset.assetnummer
        self.storing_beschrijving = self.record.get_storing_beschrijvingen()
        try:
            self.vorige_ad = self.asset.laatste_data
        except ObjectDoesNotExist:
            self.vorige_ad = None
        if self.asset.pollbaar == False:
            self.asset.pollbaar = True
        self.asset.omloop_a += self.record.omloop_a
        self.asset.omloop_b += self.record.omloop_b

    def insert_absolute_data(self):
        self.ad = AbsoluteData(
            assetnummer_id=self.asset.assetnummer,
            storing_beschrijving=self.storing_beschrijving,
            druk_a1=self.record.druk_a1,
            druk_a2=self.record.druk_a2,
            druk_b1=self.record.druk_b1,
            druk_b2=self.record.druk_b2,
            kracht_a=self.record.kracht_a,
            kracht_b=self.record.kracht_b,
            omloop_a=self.asset.omloop_a +
            self.record.omloop_a if (self.vorige_ad) else self.record.omloop_a,
            omloop_b=self.asset.omloop_b +
            self.record.omloop_b if (self.vorige_ad) else self.record.omloop_b,
            omloop_a_toegevoegd = self.record.omloop_a,
            omloop_b_toegevoegd = self.record.omloop_b,
        )
        self.ad.save()
        self.asset.laatste_data = self.ad
        self.asset.save()

    



    def maak_nieuwe_storing(self, bericht, counter=1):
        logging.info(
            f"{self.assetnummer}: Nieuwe storing aangemaakt:  {bericht}")
        new_storing = Storing(
            assetnummer_id=self.asset,
            gezien=False,
            actief=True,
            bericht=bericht,
            som=counter,
            score=0,
        )
        new_storing.score = 4 if bericht == "Druklimit overschreden" else new_storing.get_score()
        new_storing.laatste_data = self.ad
        new_storing.save()

    def storing_algoritme(self):
        #
        if (self.record.druk_a1 > self.asset.alarm_waarde_druk_a or
            self.record.druk_b1 > self.asset.alarm_waarde_druk_b or
            self.record.druk_a2 > self.asset.alarm_waarde_druk_a or
            self.record.druk_b2 > self.asset.alarm_waarde_druk_b
        ):
            try:
                qs =  Storing.objects.get(assetnummer=self.assetnummer, bericht="Druklimit overschreden", actief=True)
                qs.gezien = False
                qs.som += 1
                qs.save()

            except ObjectDoesNotExist:
                self.maak_nieuwe_storing("Druklimit overschreden")
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
                    vorige_storingen = Storing.objects.filter(assetnummer=self.assetnummer, bericht=sb, actief=True).order_by("laatste_data__tijdstip")
                    vorige_storing = vorige_storingen.first()
                except ObjectDoesNotExist:
                    vorige_storing = None
                if vorige_storing:
                    if vorige_storingen.count() > 1:
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
                    timeout = ConfiguratieElement.objects.get(configuratie=self.asset.configuratie, beschrijving=sb).timeout

                    if timeout > 0:
                        try:
                            recente_ads = AbsoluteData.objects.exclude(storing_beschrijving=[]).filter(assetnummer=self.asset.assetnummer, tijdstip__range=(
                                datetime.datetime.now() - datetime.timedelta(hours=timeout), datetime.datetime.now()))
                        except ObjectDoesNotExist:
                            recente_ads = None
                        counter = 0
                        if recente_ads:
                            for rad in recente_ads:
                                if sb in rad.storing_beschrijving:
                                    counter += 1
                                    if counter > 1 and self.record.check_storing(sb) == True: #hoevaak mag de counter voorkomen binnen de timeout
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
