from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField, ArrayField
import datetime

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    storings_pagina_filter = ArrayField(models.CharField(max_length=200), default=list, null=True)

from django.contrib.auth.signals import user_logged_in


def login_signal_method(sender, user, request, **kwargs):
    obj, created = Account.objects.get_or_create(
    user=user
)
    
user_logged_in.connect(login_signal_method)

class Asset(models.Model):
    assetnummer = models.CharField(max_length=10, primary_key=True, help_text="Het unieke nummer van deze asset")
    beschrijving = models.CharField(null=True, max_length=70, help_text="Een korte beschrijving van deze asset")
    ip_adres_logo = models.GenericIPAddressField(null=True, blank=True, help_text="Het IP-adres van de storingslogo")
    ip_adres_modem = models.GenericIPAddressField(null=True, blank=True, help_text="Het IP-adres van de H&K-modem")
    pollbaar = models.BooleanField(default=False, help_text="Is asset gereed om te pollen?")
    configuratie = models.ForeignKey("Configuratie", on_delete=models.CASCADE, null=True, default=3, help_text="Configuratie van de asset")
    weging = models.IntegerField(default=1, help_text="De zwaarte van deze asset, deze waarde wordt gebruikt voor het berekenen van de prioriteitsscore.")
    alarm_waarde_druk_a = models.IntegerField(default=750, help_text="Geef de waarde op die het 'Druklimiet'-alarm triggert voor de A-bak")
    alarm_waarde_druk_b = models.IntegerField(default=750, help_text="Geef de waarde op die het 'Druklimiet'-alarm triggert voor de B-bak")
    laatste_data = models.ForeignKey("AbsoluteData", on_delete=models.SET_NULL, null=True, editable=False)

    storing_beschrijving = ArrayField(models.CharField(max_length=200), null=True, blank=True, default=list, help_text="De storing die gemeld is tijdens de afgelopen polling.")
    druk_a1 = models.IntegerField(blank=True, default=0, help_text="De drukwaarde van de afgelopen polling.")
    druk_a2 = models.IntegerField(blank=True, default=0, help_text="De drukwaarde van de afgelopen polling.")
    druk_b1 = models.IntegerField(blank=True, default=0, help_text="De drukwaarde van de afgelopen polling.")
    druk_b2 = models.IntegerField(blank=True, default=0, help_text="De drukwaarde van de afgelopen polling.")
    kracht_a = models.IntegerField(blank=True, default=0, help_text="De krachtwaarde van de afgelopen polling.")
    kracht_b = models.IntegerField(blank=True, default=0, help_text="De krachtwaarde van de afgelopen polling.")
    omloop_a = models.IntegerField(blank=True, default=0, help_text="Het aantal omlopen van de A-bak van deze asset.")
    omloop_b = models.IntegerField(blank=True, default=0, help_text="Het aantal omlopen van de B-bak deze asset.")

    class Meta:
        ordering = ['assetnummer',]
        permissions = [("toggle_pollbaar_status", "Kan de pollbaarstatus aanpassen")]

    def __str__(self):  
        return self.assetnummer




class ConfiguratieElement(models.Model):
    inputnummer = models.SmallIntegerField(help_text="Het inputnummer van de LOGO waar het signaal is aangesloten")
    beschrijving = models.CharField(max_length=100, null=True, help_text="Korte beschrijving van het signaal / alarm dat op deze input is aangesloten.")
    urgentieniveau = models.ForeignKey("Urgentieniveau", on_delete=models.CASCADE, help_text="De zwaarte van dit alarm, deze waarde wordt gebruikt voor het berekenen van de prioriteitsscore.")
    timeout = models.IntegerField(default=24, help_text="De timeout is een tijdsperiode in uren waarbij dit alarm mag voorkomen. Als het alarm het alarm voor het eerst getriggerd wordt, gaat deze periode in. Pas als het alarm nog een keer getriggerd wordt binnen deze periode, wordt de storing weergegeven in de lijst op de homepagina. <br> Zet deze waarde op 0 om altijd het alarm weer te geven.")
    configuratie = models.ForeignKey("Configuratie", on_delete=models.DO_NOTHING, help_text="De configuratie waar dit alarm bij hoort.")
    
        

class AbsoluteData(models.Model):
    assetnummer = models.ForeignKey("Asset", on_delete=models.CASCADE)
    storing_beschrijving = ArrayField(models.CharField(max_length=200), blank=True, null=True, default=list)
    druk_a1 = models.IntegerField()
    druk_a2 = models.IntegerField()
    druk_b1 = models.IntegerField()
    druk_b2 = models.IntegerField()
    kracht_a = models.IntegerField()
    kracht_b = models.IntegerField()
    omloop_a = models.IntegerField()
    omloop_b = models.IntegerField()
    omloop_a_toegevoegd = models.IntegerField()
    omloop_b_toegevoegd = models.IntegerField()
    tijdstip = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "data"
        verbose_name_plural = "data"
        get_latest_by = "tijdstip"
        permissions = [("dashboard_access", "Heeft toegang tot het dasboard")]

    def __str__(self):
        return f"{self.assetnummer} @ {self.tijdstip.strftime('%m/%d/%Y - %H:%M:%S')}"


class SmsData(models.Model):
    ontvangen = models.DateTimeField()
    modem = models.CharField(max_length=10, default="")
    telnummer = models.CharField(max_length=15, null=True)
    storing = models.CharField(max_length=100, null=True)
    smsc = models.CharField(max_length=15, null=True)
    udh = models.BooleanField()
    inputnummer = models.IntegerField(null=True)
    status = models.CharField(max_length=15, null=True)
    alphabet = models.CharField(max_length=15, null=True)
    sent = models.DateTimeField()
    sim = models.CharField(max_length=10, null=True)
    asset = models.CharField(max_length=5, null=True)

    class Meta:
        verbose_name_plural = "sms data"
        get_latest_by = "ontvangen"

    def __str__(self):
        return f"{self.asset} @ {self.ontvangen.strftime('%m/%d/%Y - %H:%M:%S')}"

class Storing(models.Model):
    assetnummer = models.ForeignKey("Asset", on_delete=models.CASCADE)
    gezien = models.BooleanField()
    actief = models.BooleanField()
    bericht = models.CharField(max_length=100, default="")
    som = models.IntegerField(default=1)
    score = models.IntegerField(default=1)
    laatste_data = models.ForeignKey("AbsoluteData", on_delete=models.SET_NULL, null=True, editable=False)

    class Meta:
        verbose_name_plural = "storingen"

    def gezien_melden(self):
        self.gezien = True
    
    def deactiveer(self):
        self.gezien = True
        self.actief = False
    
    def get_data(self):
        records = []
        for record in AbsoluteData.objects.filter(storing=self).order_by("-tijdstip"):
            records.append(record)
        return records

    def get_score(self):
        niveau = ConfiguratieElement.objects.get(configuratie=self.assetnummer.configuratie, beschrijving=self.bericht).urgentieniveau.niveau
        return (self.som * niveau) * self.assetnummer.weging

class Configuratie(models.Model):
    naam = models.CharField(max_length=50)

    def __str__(self):
        return self.naam
    

class Urgentieniveau(models.Model):
    niveau = models.SmallIntegerField(primary_key=True, help_text="Hoe hoger het niveau, des te zwaarder alarmen met dit niveau worden gerekend.")
    beschrijving  = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.beschrijving
