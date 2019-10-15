from django.contrib import admin
from .models import *

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display=("assetnummer", "beschrijving", "bevat_logo", "ip_adres", "logo_online", "telefoonnummer")


# Register your models here.
admin.site.register(LogoMelding)
admin.site.register(ConfiguratieLijst)
admin.site.register(Urgentieniveau)