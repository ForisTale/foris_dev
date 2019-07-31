from lists.models import List, Item
from rest_framework import viewsets

from rest_api.serializers import ItemSerializer, ListSerializer


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer



