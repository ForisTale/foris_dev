from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
from lists.models import Item, List


class ItemSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        allow_blank=False, error_messages={"blank": EMPTY_ITEM_ERROR}
    )

    class Meta:
        model = Item
        fields = ("id", "list", "text")
        validators = [
            UniqueTogetherValidator(
                queryset=Item.objects.all(),
                fields=("list", "text"),
                message=DUPLICATE_ITEM_ERROR
            )
        ]


class ListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, source="item_set")

    class Meta:
        model = List
        fields = ("id", "items", "shared_with")
