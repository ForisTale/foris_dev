from rest_framework import routers
from rest_api.views import ListViewSet, ItemViewSet
# from rest_api import views
# from django.urls import path


router = routers.SimpleRouter()
router.register("lists", ListViewSet)
router.register("items", ItemViewSet)

# urlpatterns = [
#     path("lists/<int:list_id>/", views, name="api_list"),
# ]
