from rest_framework import routers
from rest_api.views import ListViewSet, ItemViewSet, api_items
from django.urls import path


router = routers.SimpleRouter()
router.register("lists", ListViewSet)
router.register("items", ItemViewSet)

urlpatterns = [
    path("tec/items/<slug:category>/", api_items, name="api_tec_items"),
]
