from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField, ArrayField
import datetime

class Asset(models.Model):
    assetnummer = models.CharField(max_length=10, primary_key=True)
    beschrijving = models.CharField(null=True, max_length=70)
    ip_adres_logo = models.GenericIPAddressField(null=True, blank=True)
    ip_adres_modem = models.GenericIPAddressField(null=True, blank=True)
    pollbaar = models.BooleanField(default=False)
    configuratie = models.ForeignKey("Configuratie", on_delete=models.CASCADE, null=True, default=3)
    weging = models.IntegerField(default=1)
    laatste_data = models.ForeignKey("AbsoluteData", on_delete=models.SET_NULL, null=True, editable=False)

    storing_beschrijving = ArrayField(models.CharField(max_length=200), null=True, blank=True, default=list)
    druk_a1 = models.IntegerField(blank=True, default=0)
    druk_a2 = models.IntegerField(blank=True, default=0)
    druk_b1 = models.IntegerField(blank=True, default=0)
    druk_b2 = models.IntegerField(blank=True, default=0)
    kracht_a = models.IntegerField(blank=True, default=0)
    kracht_b = models.IntegerField(blank=True, default=0)
    omloop_a = models.IntegerField(blank=True, default=0)
    omloop_b = models.IntegerField(blank=True, default=0)

    def __str__(self):  
        return self.assetnummer




class ConfiguratieElement(models.Model):
    inputnummer = models.SmallIntegerField()
    beschrijving = models.CharField(max_length=100, null=True)
    urgentieniveau = models.ForeignKey("Urgentieniveau", on_delete=models.CASCADE)
    timeout = models.IntegerField(default=24)
    configuratie = models.ForeignKey("Configuratie", on_delete=models.DO_NOTHING)
    
        

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
        verbose_name_plural = "absolute data"
        get_latest_by = "tijdstip"

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
    laatste_data = models.ForeignKey("AbsoluteData", on_delete=models.PROTECT, null=True, editable=False)

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
    niveau = models.SmallIntegerField(primary_key=True)
    beschrijving  = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.beschrijving
