from django.test import TestCase
from the_elder_commands.utils import ManageTestFiles, MessagesSystem


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

    def test_pop_items_messages(self):
        self.request.session.update({"items_messages": ["test"]})
        messages_system = MessagesSystem(self.request)
        message = messages_system.pop_items_messages()
        self.assertEqual(self.request.session.get("items_messages"), [])
        self.assertEqual(message, ["test"])

    def test_pop_plugins_messages(self):
        self.request.session.update({"plugins_messages": ["test"]})
        messages_system = MessagesSystem(self.request)
        message = messages_system.pop_plugins_messages()
        self.assertEqual(self.request.session.get("plugins_messages"), [])
        self.assertEqual(message, ["test"])

    def test_can_handle_missing_keys(self):
        message_system = MessagesSystem(self.request)
        item_message = message_system.pop_items_messages()
        plugin_message = message_system.pop_plugins_messages()

        self.assertEqual(item_message, [])
        self.assertEqual(plugin_message, [])

    def test_append_plugin_message(self):
        message_system = MessagesSystem(self.request)
        message_system.append_plugin_message("test")
        self.assertEqual(self.request.session.get("plugins_messages"), ["test"])

    def test_append_item_message(self):
        message_system = MessagesSystem(self.request)
        message_system.append_item_message("test")
        self.assertEqual(self.request.session.get("items_messages"), ["test"])

    def test_append_message(self):
        message_system = MessagesSystem(self.request)
        message_system._MessagesSystem__append_message("items_messages", "test")
        self.assertEqual(self.request.session.get("items_messages"), ["test"])

    def test_append_message_can_handle_list(self):
        message_system = MessagesSystem(self.request)
        message_system._MessagesSystem__append_message("plugins_messages", ["test_02"])
        self.assertEqual(self.request.session.get("plugins_messages"), ["test_02"])

    def test_append_message_can_handle_nested_list(self):
        message_system = MessagesSystem(self.request)
        message_system._MessagesSystem__append_message("items_messages", [[["test"]]])
        self.assertEqual(self.request.session.get("items_messages"), ["test"])

    def test_append_message_dont_override_older_messages(self):
        self.request.session.update({"plugins_messages": ["test01"]})
        message_system = MessagesSystem(self.request)
        message_system._MessagesSystem__append_message("plugins_messages", "test")
        self.assertEqual(self.request.session.get("plugins_messages"), ["test01", "test"])
        message_system._MessagesSystem__append_message("plugins_messages", ["other_test"])
        self.assertEqual(self.request.session.get("plugins_messages"), ["test01", "test", "other_test"])
