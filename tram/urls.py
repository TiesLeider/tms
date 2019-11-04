from django.urls import path
from . import views
 

urlpatterns = [
    path("", views.index, name="index"),
    path("insertlogodata",views.insert_logo_data, name=""),
]
