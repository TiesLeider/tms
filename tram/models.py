from djongo import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

class Asset(models.Model):
    assetnummer = models.CharField(max_length=10, primary_key=True)
    beschrijving = models.CharField(null=True, max_length=70)
    ip_adres = models.GenericIPAddressField(null=True)
    online = models.BooleanField(default=False)
    configuratie = models.ForeignKey("Configuratie", on_delete=models.CASCADE, null=True)
    weging = models.IntegerField(default=1)
    disconnections = models.IntegerField(default=0)


    def __str__(self):
        return self.assetnummer

    def heeft_laatste_storing(self):
        heeft_ls = False
        try:
            heeft_ls = (self.laatste_data is not None)
        except LogoData.DoesNotExist:
            pass
        return heeft_ls
    
class AssetLaatsteData(models.Model):
    assetnummer = models.OneToOneField("Asset", on_delete=models.DO_NOTHING)
    laatste_data = models.ForeignKey("AbsoluteData", on_delete=models.DO_NOTHING)

    def heeft_laatste_data(self):
        heeft_ld= False
        try:
            heeft_ld = (self.laatste_data is not None)
        except LogoData.DoesNotExist:
            pass
        return heeft_ld

class ConfiguratieElement(models.Model):
    inputnummer = models.SmallIntegerField()
    beschrijving = models.CharField(max_length=50, null=True)
    urgentieniveau = models.ForeignKey("Urgentieniveau", on_delete=models.CASCADE)




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
    omloop_a = models.IntegerField()
    omloop_b = models.IntegerField()
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
