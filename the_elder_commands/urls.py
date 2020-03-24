from django.urls import path
from .views import character_view, items_view, spells_view, other_view, plugins_view


app_name = "tec"

urlpatterns = [
    path("", character_view, name="character"),
    path("items/", items_view, name="items"),
    path("spells/", spells_view, name="spells"),
    path("other/", other_view, name="other"),
    path("plugins/", plugins_view, name="plugins"),
]
