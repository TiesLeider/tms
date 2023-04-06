from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ups_index"),
    path("insertdata", views.insert_data, name="insert_data"),
    path("api/get_storingen", views.get_storingen, name="get_storingen"),
    path("api/get_data", views.get_data, name="get_data")
]
