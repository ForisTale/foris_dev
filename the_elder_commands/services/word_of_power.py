from the_elder_commands.models import PluginVariants, WordsOfPower
from the_elder_commands.utils.chosen import ChosenOther
from the_elder_commands.utils.selected_plugins import SelectedPlugins


class WordsOfPowerService:
    def __init__(self, request):
        self.chosen = ChosenOther(request).get()
        self.selected = SelectedPlugins(request).get()
        self.words = self.get_words()

    def get_words(self):
        words = []
        for selected in self.selected:
            variant = PluginVariants.objects.get(instance__name=selected.get("name"), version=selected.get("version"),
                                                 language=selected.get("language"), is_esl=selected.get("is_esl"))
            model = WordsOfPower.objects.get(variant=variant)
            for word in model.words:
                form_id = f"{selected.get('load_order')}{word.get('form_id')}"
                is_selected = self.chosen.get("word" + form_id)
                word.update({"form_id": form_id, "plugin_name": selected.get("name"), "selected": is_selected})
                words.append(word)
        return words