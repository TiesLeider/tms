from django.contrib import admin
from .models import *

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display=("assetnummer",)

@admin.register(Configuratie)
class ConfiguratieAdmin(admin.ModelAdmin):
    list_display=("naam",)


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display=("asset", "storing", "niveau", "tijdstip")

# Register your models here.
