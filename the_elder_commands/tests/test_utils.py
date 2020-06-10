from django.test import TestCase
from the_elder_commands.utils import MessagesSystem, Commands, SelectedPlugins, escape_js, \
    escape_html, Skills, default_skills_race_update
from the_elder_commands.utils_for_tests import ManageTestFiles, set_up_default_nord
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
            POST = QueryDict("", mutable=True)
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
        self.assertEqual(self.request.session.get("selected"), [])

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
        self.request.POST.update(post)
        selected = SelectedPlugins(self.request)
        selected.unselect()
        one.assert_called_once()
        un_all.assert_not_called()
        one.assert_called_with("test")

    @patch("the_elder_commands.utils.SelectedPlugins._unselect_all")
    @patch("the_elder_commands.utils.SelectedPlugins._unselect_one")
    def test_unselect_for_all(self, one, un_all):
        post = QueryDict("", mutable=True)
        post.update({"unselect": "unselect_all"})
        self.request.session.update({"selected": [{"usable_name": "test"}, {"usable_name": "test_02"}]})
        self.request.POST.update(post)
        selected = SelectedPlugins(self.request)
        selected.unselect()
        un_all.assert_called_once()
        one.assert_not_called()


class EscapeJSTest(TestCase):

    def test_escape_js(self):
        string = "&<>test\u2028\u2029"
        expected = "\\u0026\\u003c\\u003etest\\u2028\\u2029"
        actual = escape_js(string)
        self.assertEqual(expected, actual)


class EscapeHTMLTest(TestCase):

    def test_escape_HTML(self):
        string = "&<>test'\""
        expected = "&amp;&lt;&gt;test&#39;&quot;"
        actual = escape_html(string)
        self.assertEqual(expected, actual)


class NewSkillsTest(TestCase):

    class FakeRequest:
        def __init__(self):
            self.session = {}

    def test_skills_save_properties_to_session(self):
        request = self.FakeRequest()
        skills = Skills(request)
        skills.save_skills({"some"})
        skills.save_desired_level(1)
        skills.save_multiplier(1.5)
        skills.save_fill_skills("true")

        self.assertDictEqual(request.session, {"skills": {"some"}, "desired_level": 1, "multiplier": 1.5,
                                               "fill_skills": "true"})

    def test_skills_can_save_race(self):
        request = self.FakeRequest()
        skills = Skills(request)
        skills.save_race("ork")
        self.assertEqual(request.session.get("race"), "ork")

    def test_can_get_race(self):
        request = self.FakeRequest()
        request.session.update({"race": "ork"})
        skills = Skills(request)
        self.assertEqual(skills.get_race(), "ork")

    def test_can_get_default_race(self):
        request = self.FakeRequest()
        skills = Skills(request)
        self.assertEqual(skills.get_race(), "nord")

    def test_can_get_skills(self):
        request = self.FakeRequest()
        request.session.update({"skills": {"Some!"}})
        skills = Skills(request)
        self.assertEqual(skills.get_skills(), {"Some!"})

    def test_have_default_skills(self):
        request = self.FakeRequest()
        skills = Skills(request)
        expected = set_up_default_nord()
        self.assertDictEqual(skills.get_skills(), expected)

    def test_can_get_desired_level(self):
        request = self.FakeRequest()
        request.session.update({"desired_level": 1})
        skills = Skills(request)
        self.assertEqual(skills.get_desired_level(), 1)

    def test_have_default_desired_level(self):
        request = self.FakeRequest()
        skills = Skills(request)
        self.assertEqual(skills.get_desired_level(), 1)

    def test_can_get_multiplier(self):
        request = self.FakeRequest()
        request.session.update({"multiplier": 2.5})
        skills = Skills(request)
        self.assertEqual(skills.get_multiplier(), 2.5)

    def test_have_default_multiplier(self):
        request = self.FakeRequest()
        skills = Skills(request)
        self.assertEqual(skills.get_multiplier(), 1.5)

    def test_can_get_fill_skills(self):
        request = self.FakeRequest()
        request.session.update({"fill_skills": "true"})
        skills = Skills(request)
        self.assertEqual(skills.get_fill_skills(), "true")

    def test_have_default_fill_skills(self):
        request = self.FakeRequest()
        skills = Skills(request)
        self.assertEqual(skills.get_fill_skills(), None)


class DefaultRaceSkillsUpdateTest(TestCase):

    def test_service_have_default_skills_method(self):
        expected = set_up_default_nord()
        actual = default_skills_race_update("nord")
        self.assertDictEqual(actual, expected)
