from .models import Plugins, PluginVariants
from .inventory import PLUGIN_TEST_DICT
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
        for key, value in data_dict.items():
            self.test_file_full_path = os.path.join(local_dir, key)
            with open(os.path.join(local_dir, key), "w+", encoding="utf-8") as file:
                file.write(str(value))

    def delete_test_files(self):
        try:
            os.remove(self.test_file_full_path)
        except (FileNotFoundError, TypeError):
            pass


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
