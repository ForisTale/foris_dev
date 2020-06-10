import copy
import os

from the_elder_commands.inventory import PLUGIN_TEST_DICT, DEFAULT_SKILLS
from the_elder_commands.models import Plugins, PluginVariants


class ManageTestFiles:
    def __init__(self):
        self.test_file_full_path = None

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


def check_test_tag(self, tag_string):
    method = getattr(self, self._testMethodName)
    tags = getattr(method, "tags", {})
    if tag_string in tags:
        return True


def select_plugin(self):
    session = self.client.session
    session.update({"selected": [{
            "name": "test 01",
            "usable_name": "test_01",
            "version": "03",
            "language": "english",
            "load_order": "A5"
        }]})
    session.save()


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


def set_up_default_nord():
    skills = copy.deepcopy(DEFAULT_SKILLS)
    skills["Combat"]["twohanded"]["default_value"] += 10
    skills["Stealth"]["speechcraft"]["default_value"] += 5
    skills["Stealth"]["lightarmor"]["default_value"] += 5
    for skill in ["block", "onehanded", "smithing"]:
        skills["Combat"][skill]["default_value"] += 5
    return skills