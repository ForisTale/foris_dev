from the_elder_commands.models import PluginVariants, Perks
from the_elder_commands.utils.chosen import ChosenOther
from the_elder_commands.utils.selected_plugins import SelectedPlugins


class PerksService:
    def __init__(self, request):
        self.chosen = ChosenOther(request).get()
        self.selected = SelectedPlugins(request).get()
        self.perks = self.get_perks()

    def get_perks(self):
        perks = []
        for selected in self.selected:
            variant = PluginVariants.objects.get(instance__name=selected.get("name"), version=selected.get("version"),
                                                 language=selected.get("language"), is_esl=selected.get("is_esl"))
            model = Perks.objects.get(variant=variant)
            for perk in model.perks:
                form_id = f"{selected.get('load_order')}{perk.get('form_id')}"
                is_selected = self.chosen.get("perk" + form_id)
                perk.update({"form_id": form_id, "plugin_name": selected.get("name"), "selected": is_selected})
                perks.append(perk)
        return perks