from djongo import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

class Asset(models.Model):
    assetnummer = models.CharField(max_length=10, primary_key=True)
    beschrijving = models.CharField(null=True, max_length=70)
    ip_adres_logo = models.GenericIPAddressField(null=True)
    ip_adres_modem = models.GenericIPAddressField(null=True)
    pollbaar = models.BooleanField(default=False)
    configuratie = models.ForeignKey("Configuratie", on_delete=models.CASCADE, null=True)
    weging = models.IntegerField(default=1)


    def __str__(self):
        return self.assetnummer

    def heeft_laatste_storing(self):
        heeft_ls = False
        try:
            heeft_ls = (self.laatste_data is not None)
        except LogoData.DoesNotExist:
            pass
        return heeft_ls


class ConfiguratieElement(models.Model):
    inputnummer = models.SmallIntegerField()
    beschrijving = models.CharField(max_length=100, null=True)
    urgentieniveau = models.ForeignKey("Urgentieniveau", on_delete=models.CASCADE)
    timeout = models.IntegerField(default=24)


class LogoData(models.Model):
    _id = models.ObjectIdField()
    assetnummer = models.ForeignKey("Asset", on_delete=models.CASCADE)
    storing = models.IntegerField()
    druk_a1 = models.IntegerField()
    druk_a2 = models.IntegerField()
    druk_b1 = models.IntegerField()
    druk_b2 = models.IntegerField()
    kracht_a = models.IntegerField()
    kracht_b = models.IntegerField()
    omloop_a = models.BigIntegerField()
    omloop_b = models.BigIntegerField()
    tijdstip = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.assetnummer} @ {self.tijdstip.strftime('%m/%d/%Y - %H:%M:%S')}"

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
        for obj in self.assetnummer.configuratie.config:
            if obj.inputnummer in self.get_hoge_inputs():
                beschrijvingen.append(obj.beschrijving)
        return beschrijvingen

    def get_storings_score(self):
        score = 0
        for obj in self.assetnummer.configuratie.config:
            if obj.inputnummer in self.get_hoge_inputs():
                score += obj.urgentieniveau.niveau
        return score
    
    def check_storing(self, storing_beschrijving):
        return storing_beschrijving in self.get_storing_beschrijvingen()
        

class AbsoluteData(models.Model):
    _id = models.ObjectIdField()
    assetnummer = models.ForeignKey("Asset", on_delete=models.CASCADE)
    storing_beschrijving = models.ListField(default=[], editable=False)
    druk_a1 = models.IntegerField()
    druk_a2 = models.IntegerField()
    druk_b1 = models.IntegerField()
    druk_b2 = models.IntegerField()
    kracht_a = models.IntegerField()
    kracht_b = models.IntegerField()
    omloop_a = models.IntegerField()
    omloop_b = models.IntegerField()
    tijdstip = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "absolute data"
        get_latest_by = "tijdstip"

    def heeft_storing(self):
        heeft_s = False
        try:
            heeft_s = (self.storing is not None)
        except AbsoluteData.DoesNotExist:
            pass
        return heeft_s

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
    laatste_data = models.ForeignKey(AbsoluteData, editable=False, default=None, on_delete=models.CASCADE)

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
        configs = self.assetnummer.configuratie.config
        for c in configs:
            if c.beschrijving == self.bericht:
                niveau = c.urgentieniveau.niveau
                break

        return (self.som * niveau) * self.assetnummer.weging

class Configuratie(models.Model):
    _id = models.ObjectIdField()
    naam = models.CharField(max_length=50)
    config = models.ArrayModelField(model_container=ConfiguratieElement)

    def __str__(self):
        return self.naam
    

class Urgentieniveau(models.Model):
    niveau = models.SmallIntegerField(primary_key=True)
    beschrijving  = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.beschrijving
