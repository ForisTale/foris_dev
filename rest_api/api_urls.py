from rest_framework import routers
from rest_api.views import ListViewSet, ItemViewSet, api_items, api_spells, api_words, api_perks
from django.urls import path


router = routers.SimpleRouter()
router.register("lists", ListViewSet)
router.register("items", ItemViewSet)

urlpatterns = [
    path("tec/items/<slug:category>/", api_items, name="api_tec_items"),
    path("tec/spells/<slug:category>/", api_spells, name="api_tec_spells"),
    path("tec/wordsofpower/", api_words, name="api_tec_words"),
    path("tec/perks/", api_perks, name="api_tec_perks"),
]
