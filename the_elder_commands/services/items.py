from the_elder_commands.models import PluginVariants, Weapons, Armors, Ammo, Books, Ingredients, Alchemy, Miscellaneous, \
    Keys, Scrolls, SoulsGems
from the_elder_commands.utils.chosen import ChosenItems
from the_elder_commands.utils.selected_plugins import SelectedPlugins


class ItemsService:
    def __init__(self, request, category):
        self.chosen = ChosenItems(request).get()
        self.selected = SelectedPlugins(request).get()
        self.items = self.get_items(category)

    def get_items(self, category):
        items = []
        for selected in self.selected:
            variant = PluginVariants.objects.get(instance__name=selected.get("name"), version=selected.get("version"),
                                                 language=selected.get("language"), is_esl=selected.get("is_esl"))
            items_model = self.get_item_model(category, variant)
            for item in items_model.items:
                form_id = f"{selected.get('load_order')}{item.get('form_id')}"
                quantity = self.chosen.get(form_id, "")
                item.update({"form_id": form_id, "plugin_name": selected.get("name"), "quantity": quantity,
                             "selected": quantity != ""})
                items.append(item)
        return items

    @staticmethod
    def get_item_model(category, variant):
        if category == "WEAP":
            return Weapons.objects.get(variant=variant)
        elif category == "ARMO":
            return Armors.objects.get(variant=variant)
        elif category == "AMMO":
            return Ammo.objects.get(variant=variant)
        elif category == "BOOK":
            return Books.objects.get(variant=variant)
        elif category == "INGR":
            return Ingredients.objects.get(variant=variant)
        elif category == "ALCH":
            return Alchemy.objects.get(variant=variant)
        elif category == "MISC":
            return Miscellaneous.objects.get(variant=variant)
        elif category == "KEYM":
            return Keys.objects.get(variant=variant)
        elif category == "SCRL":
            return Scrolls.objects.get(variant=variant)
        elif category == "SLGM":
            return SoulsGems.objects.get(variant=variant)