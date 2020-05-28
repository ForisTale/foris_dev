from django.test import TestCase
from the_elder_commands.utils import ManageTestFiles, MessagesSystem, Commands, SelectedPlugins
from unittest.mock import patch
from django.http import QueryDict


class ManageTestFilesTest(TestCase):

    def test_unpack_dict(self):
        dictionary = {1: "2"}
        actual_key, actual_val = ManageTestFiles.unpack_dict(dictionary)
        self.assertEqual((actual_key, actual_val), (1, "2"))


class MessageSystemTest(TestCase):

    def setUp(self):
        class FakeRequest:
            session = {}

        self.request = FakeRequest()

    def test_append_item_message(self):
        message_system = MessagesSystem(self.request)
        message_system.append_item("test")
        self.assertEqual(self.request.session.get("items_messages"), ["test"])

    def test_pop_items_messages(self):
        self.request.session.update({"items_messages": ["test"]})
        messages_system = MessagesSystem(self.request)
        message = messages_system.pop_items()
        self.assertEqual(self.request.session.get("items_messages"), [])
        self.assertEqual(message, ["test"])

    def test_append_plugin_message(self):
        message_system = MessagesSystem(self.request)
        message_system.append_plugin("test")
        self.assertEqual(self.request.session.get("plugins_messages"), ["test"])

    def test_pop_plugins_messages(self):
        self.request.session.update({"plugins_messages": ["test"]})
        messages_system = MessagesSystem(self.request)
        message = messages_system.pop_plugins()
        self.assertEqual(self.request.session.get("plugins_messages"), [])
        self.assertEqual(message, ["test"])

    def test_append_skills_messages(self):
        message_system = MessagesSystem(self.request)
        message_system.append_skills("test")
        self.assertEqual(self.request.session.get("skills_messages"), ["test"])

    def test_pop_skills_messages(self):
        self.request.session.update({"skills_messages": ["test"]})
        messages_system = MessagesSystem(self.request)
        message = messages_system.pop_skills()
        self.assertEqual(self.request.session.get("skills_messages"), [])
        self.assertEqual(message, ["test"])

    def test_pop_messages(self):
        self.request.session.update({"messages": ["test"]})
        messages_system = MessagesSystem(self.request)
        message = messages_system._pop_messages("messages")
        self.assertEqual(self.request.session.get("messages"), [])
        self.assertEqual(message, ["test"])

    def test_can_handle_missing_keys(self):
        message_system = MessagesSystem(self.request)
        item_message = message_system.pop_items()
        plugin_message = message_system.pop_plugins()
        skills_message = message_system.pop_skills()

        self.assertEqual(item_message, [])
        self.assertEqual(plugin_message, [])
        self.assertEqual(skills_message, [])

    def test_append_message(self):
        message_system = MessagesSystem(self.request)
        message_system._append_message("items_messages", "test")
        self.assertEqual(self.request.session.get("items_messages"), ["test"])

    def test_append_message_can_handle_list(self):
        message_system = MessagesSystem(self.request)
        message_system._append_message("plugins_messages", ["test_02"])
        self.assertEqual(self.request.session.get("plugins_messages"), ["test_02"])

    def test_append_message_can_handle_nested_list(self):
        message_system = MessagesSystem(self.request)
        message_system._append_message("items_messages", [[["test"]], "test02"])
        self.assertEqual(self.request.session.get("items_messages"), ["test", "test02"])

    def test_append_message_dont_override_older_messages(self):
        self.request.session.update({"plugins_messages": ["test01"]})
        message_system = MessagesSystem(self.request)
        message_system._append_message("plugins_messages", "test")
        self.assertEqual(self.request.session.get("plugins_messages"), ["test01", "test"])
        message_system._append_message("plugins_messages", ["other_test"])
        self.assertEqual(self.request.session.get("plugins_messages"), ["test01", "test", "other_test"])


class CommandsTest(TestCase):

    def setUp(self):
        class FakeRequest:
            session = {}

        self.request = FakeRequest()

    def test_can_set_skills_commands(self):
        commands = Commands(self.request)
        commands.set_skills(["command"])
        self.assertEqual(self.request.session.get("skills_commands"), ["command"])

    def test_can_set_items_commands(self):
        commands = Commands(self.request)
        commands.set_items({"item_01": "1"})
        self.assertEqual(self.request.session.get("items_commands"), ["player.additem item_01 1"])

    def test_get_commands(self):
        self.request.session.update({"skills_commands": ["skills"], "items_commands": ["items"]})
        commands = Commands(self.request)
        actual = commands.get_commands()
        expected = ["skills", "items"]

        self.assertEqual(expected, actual)
        self.assertEqual(self.request.session.get("skills_commands"), ["skills"])
        self.assertEqual(self.request.session.get("items_commands"), ["items"])

    def test_get_commands_can_handle_empty_keys(self):
        commands = Commands(self.request)
        actual = commands.get_commands()
        self.assertEqual([], actual)


class SelectedPluginsTest(TestCase):

    def setUp(self):
        class FakeRequest:
            session = {}

        self.request = FakeRequest()

    def test_plugins_are_selected(self):
        selected = SelectedPlugins(self.request)

        self.assertEqual(selected.exist(), False)

        self.request.session.update({"selected": ["plugin"]})
        self.assertEqual(selected.exist(), True)

    def test_set(self):
        selected = SelectedPlugins(self.request)
        selected.set(["one"])
        self.assertEqual(self.request.session.get("selected"), ["one"])

    def test_get(self):
        selected = SelectedPlugins(self.request)
        actual = selected.get()
        self.assertEqual([], actual)

        self.request.session.update({"selected": ["one"]})
        actual = selected.get()
        self.assertEqual(["one"], actual)

    def test_unselect_one(self):
        self.request.session.update({"selected": [{"usable_name": "test"}, {"usable_name": "test_02"}]})
        selected = SelectedPlugins(self.request)
        selected._unselect_one("test")
        self.assertEqual(self.request.session.get("selected"), [{"usable_name": "test_02"}])

    def test_unselect_one_can_handle_missing_key(self):
        selected = SelectedPlugins(self.request)
        selected._unselect_one("test")
        self.assertEqual(self.request.session.get("selected"), None)

    def test_unselect_all(self):
        self.request.session.update({"selected": [{"usable_name": "test"}, {"usable_name": "test_02"}]})
        selected = SelectedPlugins(self.request)
        selected._unselect_all()
        self.assertEqual(self.request.session.get("selected"), [])

    @patch("the_elder_commands.utils.SelectedPlugins._unselect_all")
    @patch("the_elder_commands.utils.SelectedPlugins._unselect_one")
    def test_unselect_for_one(self, one, un_all):
        post = QueryDict("", mutable=True)
        post.update({"unselect": "test"})
        self.request.session.update({"selected": [{"usable_name": "test"}, {"usable_name": "test_02"}]})
        selected = SelectedPlugins(self.request)
        selected.unselect(post)
        one.assert_called_once()
        un_all.assert_not_called()
        one.assert_called_with("test")

    @patch("the_elder_commands.utils.SelectedPlugins._unselect_all")
    @patch("the_elder_commands.utils.SelectedPlugins._unselect_one")
    def test_unselect_for_all(self, one, un_all):
        post = QueryDict("", mutable=True)
        post.update({"unselect": "unselect_all"})
        self.request.session.update({"selected": [{"usable_name": "test"}, {"usable_name": "test_02"}]})
        selected = SelectedPlugins(self.request)
        selected.unselect(post)
        un_all.assert_called_once()
        one.assert_not_called()
