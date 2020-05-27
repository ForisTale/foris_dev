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
        self.items_key = "items_messages"
        self.plugins_key = "plugins_messages"

    def pop_items_messages(self):
        message = self.request.session.get(self.items_key, [])
        self.request.session.update({self.items_key: []})
        return message

    def pop_plugins_messages(self):
        message = self.request.session.get(self.plugins_key, [])
        self.request.session.update({self.plugins_key: []})
        return message

    def append_plugin_message(self, message):
        self.__append_message(self.plugins_key, message)

    def append_item_message(self, message):
        self.__append_message(self.items_key, message)

    def __append_message(self, key, message):
        if type(message) == list:
            try:
                self.__append_message(key, message.pop(0))
                self.__append_message(key, message)
            except IndexError:
                pass
        else:
            new_message = self.request.session.get(key, [])
            new_message.append(message)
            self.request.session.update({key: new_message})
