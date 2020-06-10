from .inventory import RACES_EXTRA_SKILLS, DEFAULT_SKILLS
import copy


class MessagesSystem:
    def __init__(self, request):
        self.request = request
        self._items_key = "items_messages"
        self._plugins_key = "plugins_messages"
        self._skills_key = "skills_messages"

    def append_plugin(self, message):
        self._append_message(self._plugins_key, message)

    def append_item(self, message):
        self._append_message(self._items_key, message)

    def append_skills(self, message):
        self._append_message(self._skills_key, message)

    def _append_message(self, key, message):
        if type(message) == list:
            try:
                self._append_message(key, message.pop(0))
                self._append_message(key, message)
            except IndexError:
                pass
        else:
            new_message = self.request.session.get(key, [])
            new_message.append(message)
            self.request.session.update({key: new_message})

    def pop_items(self):
        return self._pop_messages(self._items_key)

    def pop_plugins(self):
        return self._pop_messages(self._plugins_key)

    def pop_skills(self):
        return self._pop_messages(self._skills_key)

    def _pop_messages(self, key):
        message = self.request.session.get(key, [])
        self.request.session.update({key: []})
        return message


class Commands:
    def __init__(self, request):
        self.request = request
        self._skills_key = "skills_commands"
        self._items_key = "items_commands"

    def set_skills(self, commands):
        self.request.session.update({self._skills_key: commands})

    def set_items(self, items):
        commands = []
        for form_id, quantity in items.items():
            commands.append(f"player.additem {form_id} {quantity}")
        self.request.session.update({self._items_key: commands})

    def get_commands(self):
        commands = []
        commands += self.request.session.get(self._skills_key, [])
        commands += self.request.session.get(self._items_key, [])
        return commands


class ChosenItems:
    def __init__(self, request):
        self.request = request
        self._key = "chosen_items"

    def set(self, items):
        self.request.session.update({self._key: items})

    def get(self):
        return self.request.session.get(self._key, {})


class SelectedPlugins:
    def __init__(self, request):
        self.request = request
        self._key = "selected"
        self._unselect_key = "unselect"

    def exist(self):
        return self.request.session.get(self._key, []) != []

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


def escape_js(string):
    escape = {'&': '\\u0026', '<': '\\u003c', '>': '\\u003e', '\u2028': '\\u2028', '\u2029': '\\u2029'}
    for unsafe, safe in escape.items():
        string = string.replace(unsafe, safe)
    return string


def escape_html(string):
    escape = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '\'': '&#39;', '\"': '&quot;'}
    for unsafe, safe in escape.items():
        string = string.replace(unsafe, safe)
    return string


def default_skills_race_update(race):
    skills_tree = copy.deepcopy(DEFAULT_SKILLS)
    for category, skills in RACES_EXTRA_SKILLS[race][10].items():
        skills_tree[category][skills]["default_value"] += 10
    for category, skills in RACES_EXTRA_SKILLS[race][5].items():
        for skill in skills:
            skills_tree[category][skill]["default_value"] += 5
    return skills_tree


class Skills:
    def __init__(self, request):
        self.request = request
        self._race_key = "race"
        self._default_race = "nord"
        self._skills_key = "skills"
        self._desired_level_key = "desired_level"
        self._multiplier_key = "multiplier"
        self._fill_skills_key = "fill_skills"

    def save_skills(self, skills):
        self.request.session.update({self._skills_key: skills})

    def save_desired_level(self, desired_level):
        self.request.session.update({self._desired_level_key: desired_level})

    def save_multiplier(self, multiplier):
        self.request.session.update({self._multiplier_key: multiplier})

    def save_race(self, race):
        self.request.session.update({self._race_key: race})

    def save_fill_skills(self, value):
        self.request.session.update({self._fill_skills_key: value})

    def get_race(self):
        return self.request.session.get(self._race_key, self._default_race)

    def get_skills(self):
        return self.request.session.get(self._skills_key, default_skills_race_update(self._default_race))

    def get_desired_level(self):
        return self.request.session.get(self._desired_level_key, 1)

    def get_multiplier(self):
        return self.request.session.get(self._multiplier_key, 1.5)

    def get_fill_skills(self):
        return self.request.session.get(self._fill_skills_key)
