from the_elder_commands.inventory.messages import INCORRECT_LOAD_ORDER, NO_PLUGIN_SELECTED
from the_elder_commands.models import Plugins
from the_elder_commands.utils.selected_plugins import SelectedPlugins
import json


class SelectedPluginsForm:
    def __init__(self, request):
        self.request = request
        self.errors = []
        self.data = self.get_data(request)

        self.check_data_not_empty()
        self.clean_load_order()
        if self.is_valid():
            self.collect_selected()

    def clean_load_order(self):
        for plugin in self.data:
            load_order = plugin.get("load_order", "")
            length = len(load_order)
            if length == 2 and not self.is_esl(plugin):
                if load_order.isalnum():
                    continue
            elif length == 5 and self.is_esl(plugin):
                if load_order.isalnum():
                    if load_order[:2] in ["FE", "FF"]:
                        continue

            self.errors.append(INCORRECT_LOAD_ORDER)

    def is_esl(self, plugin):
        variant = self.split_variant(plugin)
        return bool(variant[2])

    def is_valid(self):
        return self.errors == []

    def collect_selected(self):
        collected = []
        for plugin in self.data:
            usable_name = plugin.get("name")
            variant = self.split_variant(plugin)
            collected.append({
                "name": self.get_name(usable_name),
                "usable_name": usable_name,
                "version": variant[0],
                "language": variant[1],
                "is_esl": self.is_esl(plugin),
                "load_order": plugin.get("load_order")
            })
        SelectedPlugins(self.request).set(collected)

    @staticmethod
    def split_variant(plugin):
        plugin_variants = plugin.get("variant", "")
        variant = plugin_variants.split("&")
        return variant

    @staticmethod
    def get_name(usable_name):
        plugin = Plugins.objects.get(usable_name=usable_name)
        return plugin.name

    @staticmethod
    def get_data(request):
        post = request.POST.get("selected_plugins")
        converted_post = json.loads(post)
        return converted_post

    def check_data_not_empty(self):
        if not self.data:
            self.errors.append(NO_PLUGIN_SELECTED)
