from the_elder_commands.inventory import INCORRECT_LOAD_ORDER
from the_elder_commands.models import Plugins
from the_elder_commands.utils import SelectedPlugins


class SelectedPluginsForm:
    def __init__(self, request):
        self.data = request.POST.copy()
        self.request = request
        self.errors = []

        self.clean_load_order()
        if self.is_valid():
            self.collect_selected()

    def clean_load_order(self):
        selected = self.data.getlist("selected", [])
        for usable_name in selected:
            if usable_name == "":
                continue

            load_order = self.data.get(f"{usable_name}_load_order", "")
            length = len(load_order)
            if length == 2 and not self.is_esl(usable_name):
                if load_order.isalnum():
                    continue
            elif length == 5 and self.is_esl(usable_name):
                if load_order.isalnum():
                    if load_order[:2] in ["FE", "FF"]:
                        continue

            self.errors.append(INCORRECT_LOAD_ORDER)

    def is_esl(self, usable_name):
        variant = self.split_variant(usable_name)
        return bool(variant[2])

    def is_valid(self):
        return self.errors == []

    def collect_selected(self):
        selected_from_post = self.data.getlist("selected", [])
        collected = []
        for usable_name in selected_from_post:
            if usable_name == "":
                continue
            variant = self.split_variant(usable_name)
            collected.append({
                "name": self.get_name(usable_name),
                "usable_name": usable_name,
                "version": variant[0],
                "language": variant[1],
                "is_esl": self.is_esl(usable_name),
                "load_order": self.data.get(f"{usable_name}_load_order")
            })
        SelectedPlugins(self.request).set(collected)

    def split_variant(self, usable_name):
        variant = self.request.POST.get(f"{usable_name}_variant")
        return variant.split("&")

    @staticmethod
    def get_name(usable_name):
        plugin = Plugins.objects.get(usable_name=usable_name)
        return plugin.name