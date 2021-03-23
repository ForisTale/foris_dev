from django.core.exceptions import ObjectDoesNotExist

from the_elder_commands.models import PluginVariants


class SelectedPlugins:
    def __init__(self, request):
        self.request = request
        self._key = "selected"
        self._unselect_key = "unselect"

    def exist(self):
        selected_plugins = self.request.session.get(self._key)
        if selected_plugins:
            for selected in selected_plugins:
                try:
                    PluginVariants.objects.get(instance__name=selected.get("name"), language=selected.get("language"),
                                               version=selected.get("version"), is_esl=selected.get("is_esl"))
                except ObjectDoesNotExist:
                    self.request.session.update({self._key: []})
                    return False
            return True
        return False

    def set(self, selected):
        self.request.session.update({self._key: selected})

    def get(self):
        return self.request.session.get(self._key, [])

    def _unselect_one(self, usable_name):
        all_selected = self.request.session.get(self._key, [])
        for selected in all_selected:
            if selected.get("usable_name") == usable_name:
                all_selected.remove(selected)
        self.request.session.update({self._key: all_selected})

    def _unselect_all(self):
        self.request.session.update({self._key: []})

    def unselect(self):
        post = self.request.POST
        usable_name = post.get(self._unselect_key)
        if usable_name == "unselect_all":
            self._unselect_all()
        else:
            self._unselect_one(usable_name)