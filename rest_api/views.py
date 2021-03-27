from rest_api.serializers import ItemSerializer, ListSerializer
from lists.models import List, Item
from rest_framework import viewsets

from django.http import JsonResponse
from the_elder_commands.services.perks import PerksService
from the_elder_commands.services.word_of_power import WordsOfPowerService
from the_elder_commands.services.spells import SpellsService
from the_elder_commands.services.items import ItemsService


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


def api_words(request):
    service = WordsOfPowerService(request)
    return JsonResponse(service.words, safe=False)


def api_perks(request):
    service = PerksService(request)
    return JsonResponse(service.perks, safe=False)
