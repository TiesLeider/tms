from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin, ImportExportModelAdmin

admin.site.site_header = "TMS Beheer"

#TODO Verzenden gebruiker gegevens naar Email.



class AbsoluteDataResource(resources.ModelResource):
    class Meta:
        model = AbsoluteData

class UrgentieniveauResource(resources.ModelResource):
    class Meta:
        skip_unchanged = True
        report_skipped = True
        model = Urgentieniveau
        import_id_fields = ["niveau"]

class ConfiguratieElementResource(resources.ModelResource):
    class Meta:
        skip_unchanged = True
        report_skipped = True
        model = ConfiguratieElement


class ConfiguratieElementInline(admin.TabularInline):
    model = ConfiguratieElement


class AssetResource(resources.ModelResource):
    class Meta:
        skip_unchanged = True
        report_skipped = True
        model = Asset
        import_id_fields = ["assetnummer"]
        exclude = ("storing_beschrijving", "laatste_data", "omloop_a", "omloop_b")

class StoringResource(resources.ModelResource):
    class Meta:
        model = Storing

class ConfiguratieResource(resources.ModelResource):

    class Meta:
        model = Configuratie
    
class AssetAdmin(ImportExportActionModelAdmin):
    list_display=("assetnummer", "beschrijving", "ip_adres_logo", "pollbaar")
    resource_class = AssetResource


@admin.register(AbsoluteData)
#class AbsoluteDataAdmin(admin.ModelAdmin):
class AbsoluteDataAdmin(ImportExportModelAdmin):
    list_display=("assetnummer_id", "tijdstip", "storing_beschrijving", "omloop_a", "omloop_b", "druk_a1", "druk_a2", "druk_b1", "druk_b2")
    list_filter=("assetnummer_id"),

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display=("id",)

@admin.register(SmsData)
class SmsDataAdmin(admin.ModelAdmin):
    list_display=("asset", "storing", "ontvangen",)

@admin.register(Configuratie)
class ConfiguratieAdmin(ImportExportActionModelAdmin):
    list_display=("naam",)
    inlines = [ConfiguratieElementInline,]
    resource_class = ConfiguratieResource

@admin.register(Storing)
class StoringAdmin(ExportActionModelAdmin):
    list_display=("id", "assetnummer", "actief", "gezien")

@admin.register(ConfiguratieElement)
class ConfiguratieElemenentAdmin(ImportExportActionModelAdmin):
    list_display=("id", "inputnummer", "beschrijving", "urgentieniveau", "timeout", "configuratie")
    resource_class = ConfiguratieElementResource

@admin.register(Urgentieniveau)
class UrgentieniveauAdmin(ImportExportActionModelAdmin):
    resource_class = UrgentieniveauResource

# Register your models here.
# admin.site.register(LogoMelding)
# admin.site.register(Configuratie)
admin.site.register(Asset, AssetAdmin)