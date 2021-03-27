from the_elder_commands.models import PluginVariants, AlterationSpells, DestructionSpells, ConjurationSpells, \
    IllusionSpells, RestorationSpells, OtherSpells
from the_elder_commands.utils.chosen import ChosenSpells
from the_elder_commands.utils.selected_plugins import SelectedPlugins


class SpellsService:
    def __init__(self, request, category):
        self.chosen = ChosenSpells(request).get()
        self.selected = SelectedPlugins(request).get()
        self.spells = self.get_spells(category)

    def get_spells(self, category):
        spells = []
        for selected in self.selected:
            variant = PluginVariants.objects.get(instance__name=selected.get("name"), version=selected.get("version"),
                                                 language=selected.get("language"), is_esl=selected.get("is_esl"))
            model = self.get_spells_model(category, variant)
            for spell in model.spells:
                form_id = f"{selected.get('load_order')}{spell.get('form_id')}"
                is_selected = self.chosen.get(form_id)
                spell.update({"form_id": form_id, "plugin_name": selected.get("name"), "selected": is_selected})
                spells.append(spell)
        return spells

    @staticmethod
    def get_spells_model(category, variant):
        if category == "alteration":
            return AlterationSpells.objects.get(variant=variant)
        elif category == "destruction":
            return DestructionSpells.objects.get(variant=variant)
        elif category == "conjuration":
            return ConjurationSpells.objects.get(variant=variant)
        elif category == "illusion":
            return IllusionSpells.objects.get(variant=variant)
        elif category == "restoration":
            return RestorationSpells.objects.get(variant=variant)
        elif category == "other":
            return OtherSpells.objects.get(variant=variant)