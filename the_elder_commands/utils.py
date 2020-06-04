from .models import Plugins, PluginVariants
from .inventory import PLUGIN_TEST_DICT, RACES_EXTRA_SKILLS, DEFAULT_SKILLS
import copy
import os


class ManageTestFiles:
    def __init__(self):
        self.test_file_full_path = None

    def check_test_tag(self, tag_string):
        method = getattr(self, self._testMethodName)
        tags = getattr(method, "tags", {})
        if tag_string in tags:
            return True

    def create_test_files(self, data_dict):
        local_dir = os.path.dirname(os.path.abspath(__file__))
        key, value = self.unpack_dict(data_dict)
        self.test_file_full_path = os.path.join(local_dir, key)
        with open(os.path.join(local_dir, key), "w+", encoding="utf-8") as file:
            file.write(str(value))

    def delete_test_files(self):
        try:
            os.remove(self.test_file_full_path)
        except (FileNotFoundError, TypeError):
            pass

    @staticmethod
    def unpack_dict(dictionary):
        dict_view = dictionary.items()
        tuples_list = list(dict_view)
        dict_tuple = tuples_list[0]
        return dict_tuple[0], dict_tuple[1]


def populate_plugins_table():
    for index in range(4):
        plugin = Plugins.objects.create(name="test 0" + str(index+1), usable_name="test_0" + str(index+1))
        plugin.save()
        corrected_dict = copy.deepcopy(PLUGIN_TEST_DICT)
        corrected_dict.pop("isEsl")
        for num in range(4):
            form = PluginVariants.objects.create(
                instance=plugin,
                version="0" + str(num+1),
                language="english",
                plugin_data=corrected_dict
            )
            form.save()


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

    def unselect(self, post):
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


def set_up_default_nord():
    skills = copy.deepcopy(DEFAULT_SKILLS)
    skills["Combat"]["twohanded"]["default_value"] += 10
    skills["Stealth"]["speechcraft"]["default_value"] += 5
    skills["Stealth"]["lightarmor"]["default_value"] += 5
    for skill in ["block", "onehanded", "smithing"]:
        skills["Combat"][skill]["default_value"] += 5
    return skills


def default_race_skills_update(race):
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
        return self.request.session.get(self._skills_key, default_race_skills_update(self._default_race))

    def get_desired_level(self):
        return self.request.session.get(self._desired_level_key, 1)

    def get_multiplier(self):
        return self.request.session.get(self._multiplier_key, 1.5)

    def get_fill_skills(self):
        return self.request.session.get(self._fill_skills_key)
