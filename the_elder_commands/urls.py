from django.urls import path
from .views import character_view


app_name = "tec"

urlpatterns = [
    path("", character_view, name="character"),
]
