from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

class AssetResource(resources.ModelResource):

    class Meta:
        model = Asset
    
class AssetAdmin(ImportExportActionModelAdmin):
    list_display=("assetnummer", "beschrijving", "ip_adres", "online", "disconnections")
    resource_class = AssetResource

@admin.register(LogoData)
class LogoDataAdmin(admin.ModelAdmin):
    list_display=("assetnummer_id", "tijdstip", "storing", "omloop_a", "omloop_b")
    list_filter=("assetnummer_id"),

@admin.register(AbsoluteData)
class AbsoluteDataAdmin(admin.ModelAdmin):
    list_display=("assetnummer_id", "tijdstip", "storing_beschrijving", "omloop_a", "omloop_b")
    list_filter=("assetnummer_id"),

@admin.register(SmsData)
class SmsDataAdmin(admin.ModelAdmin):
    list_display=("asset", "storing", "ontvangen",)

@admin.register(Configuratie)
class ConfiguratieAdmin(admin.ModelAdmin):
    list_display=("naam",)

@admin.register(Storing)
class StoringAdmin(admin.ModelAdmin):
    list_display=("id", "assetnummer", "actief", "gezien")


# Register your models here.
# admin.site.register(LogoMelding)
# admin.site.register(Configuratie)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Urgentieniveau)