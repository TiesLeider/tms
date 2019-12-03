from django.urls import path
from . import views
 

urlpatterns = [
    path("", views.index, name="index"),
    path("insertlogodata",views.insert_logo_data, name="insert_logo_data"),
    path("insertlogoonline",views.insert_logo_online, name="insert_logo_online"),
    path("storing/<int:storing_id>/gezien",views.storing_gezien, name="storing_gezien"),
    path("storing/<int:storing_id>/deactiveer",views.deactiveer_storing, name="storing_deactiveren"),
    path("storingen", views.alle_storingen, name="alle_storingen"),
    path("asset/<str:assetnummer>", views.asset_index, name="asset_index"),
    path("asset/<str:assetnummer>/resetteller", views.asset.reset_teller_standen, name="asset_reset_teller"),
    path("asset/resettelleralle", views.asset.reset_teller_alle, name="asset_reset_alle"),
    path("api/omlopen/<str:assetnummer>/<str:van_datum>/<str:tot_datum>", views.api.get_omlopen, name="get_omlopen"),
    path("api/alle_actieve_storingen/", views.get_actieve_storingen, name="alle_actieve_storingen")
]