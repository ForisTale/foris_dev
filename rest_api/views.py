from rest_api.serializers import ItemSerializer, ListSerializer
from lists.models import List, Item
from rest_framework import viewsets

from django.http import JsonResponse
from the_elder_commands.services import ItemsService, SpellsService


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


def api_items(request, category):
    items_service = ItemsService(request, category)
    return JsonResponse(items_service.items, safe=False)


def api_spells(request, category):
    service = SpellsService(request, category)
    return JsonResponse(service.spells, safe=False)
