from django.test import TestCase
from the_elder_commands.utils.commands import Commands
from the_elder_commands.utils.selected_plugins import SelectedPlugins
from the_elder_commands.utils.escape_js import escape_js
from the_elder_commands.utils.escape_html import escape_html
from the_elder_commands.utils.convert_value_post import convert_value_post, convert_value_input
from the_elder_commands.utils.skills import Skills
from the_elder_commands.utils.defauld_skills_race_update import default_skills_race_update
from the_elder_commands.utils.chosen import BaseChosen
from the_elder_commands.utils.check_recaptcha import check_recaptcha
from the_elder_commands.utils.messages_system import MessagesSystem
from the_elder_commands.utils_for_tests.setup_default_nord import setup_default_nord
from the_elder_commands.utils_for_tests.populate_plugins_table import populate_plugins_table
from the_elder_commands.utils_for_tests.fake_request import FakeRequest
from the_elder_commands.utils_for_tests.fake_response import FakeResponse
from the_elder_commands.utils_for_tests.manage_test_files import ManageTestFiles
from unittest.mock import patch, MagicMock
from django.http import QueryDict
from django.conf import settings


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

    def test_append_spells_messages(self):
        message_system = MessagesSystem(self.request)
        message_system.append_spells("test")
        self.assertEqual(self.request.session.get("spells_messages"), ["test"])

    def test_pop_spells_messages(self):
        self.request.session.update({"spells_messages": ["test"]})
        messages_system = MessagesSystem(self.request)
        message = messages_system.pop_spells()
        self.assertEqual(self.request.session.get("spells_messages"), [])
        self.assertEqual(message, ["test"])

    def test_append_other_messages(self):
        message_system = MessagesSystem(self.request)
        message_system.append_other("test")
        self.assertEqual(self.request.session.get("other_messages"), ["test"])

    def test_pop_other_messages(self):
        self.request.session.update({"other_messages": ["test"]})
        messages_system = MessagesSystem(self.request)
        message = messages_system.pop_other()
        self.assertEqual(self.request.session.get("other_messages"), [])
        self.assertEqual(message, ["test"])

    def test_append_contact_messages(self):
        message_system = MessagesSystem(self.request)
        message_system.append_contact("test")
        self.assertEqual(self.request.session.get("contact_messages"), ["test"])

    def test_pop_contact_messages(self):
        self.request.session.update({"contact_messages": ["test"]})
        messages_system = MessagesSystem(self.request)
        message = messages_system.pop_contact()
        self.assertEqual(self.request.session.get("contact_messages"), [])
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

    def test_can_set_spells_commands(self):
        commands = Commands(self.request)
        commands.set_spells({"spell_01": True})
        self.assertEqual(self.request.session.get("spells_commands"), ["player.addspell spell_01"])

    # coc should be always last in commands!
    def test_can_set_other_commands(self):
        commands = Commands(self.request)
        commands.set_other({"location": "Winterhold", "gold": "1", "dragon_souls": "1", "health": "110",
                            "magicka": "120", "stamina": "130", "carry_weight": "100", "movement_speed": "120",
                            "word12345678": "on", "perk87654321": "on"})
        expected = ["player.additem 0000000F 1", "player.modav dragonsouls 1",
                    "player.modav health 110", "player.modav magicka 120", "player.modav stamina 130",
                    "player.modav carryweight 100", "player.setav speedmult 120", "player.teachword 12345678",
                    "player.addperk 87654321", "coc WinterholdExterior01"]
        actual = self.request.session.get("other_commands")
        self.assertEqual(expected, actual)

    # other should be always last in commands!
    def test_get_commands(self):
        self.request.session.update({"skills_commands": ["skills"], "items_commands": ["items"],
                                     "spells_commands": ["spells"], "other_commands": ["other"]})
        commands = Commands(self.request)
        actual = commands.get_commands()
        expected = ["skills", "items", "spells", "other"]
        self.assertEqual(expected, actual)

    def test_get_commands_can_handle_empty_keys(self):
        commands = Commands(self.request)
        actual = commands.get_commands()
        self.assertEqual([], actual)


class SelectedPluginsTest(TestCase):

    def setUp(self):
        populate_plugins_table()

        class FakeRequest:
            POST = QueryDict("", mutable=True)
            session = {"selected": [{"usable_name": "test_01", "language": "english", "version": "01",
                                     "is_esl": False, "name": "test 01"}]}
        self.request = FakeRequest()

    def test_exist_return_true_when_plugins_are_selected(self):
        selected = SelectedPlugins(self.request)
        self.assertEqual(selected.exist(), True)

        self.request.session = {}
        self.assertEqual(selected.exist(), False)

    def test_exist_check_if_all_selected_plugins_exist_in_database(self):
        self.request.session.update({"selected": [{"usable_name": "wrong_name", "language": "english", "version": "01",
                                     "is_esl": False, "name": "wrong name"}]})
        selected = SelectedPlugins(self.request)
        self.assertEqual(selected.exist(), False)
        self.assertEqual(self.request.session.get("selected"), [])

    def test_set(self):
        selected = SelectedPlugins(self.request)
        selected.set(["one"])
        self.assertEqual(self.request.session.get("selected"), ["one"])

    def test_get(self):
        selected = SelectedPlugins(self.request)
        actual = selected.get()
        self.assertEqual([{'usable_name': 'test_01', 'language': 'english', 'version': '01', 'is_esl': False,
                           'name': 'test 01'}], actual)

    def test_get_default_return(self):
        self.request.session = {}
        selected = SelectedPlugins(self.request)
        actual = selected.get()
        self.assertEqual([], actual)

    def test_unselect_one(self):
        self.request.session.update({"selected": [{"usable_name": "test"}, {"usable_name": "test_02"}]})
        selected = SelectedPlugins(self.request)
        selected._unselect_one("test")
        self.assertEqual(self.request.session.get("selected"), [{"usable_name": "test_02"}])

    def test_unselect_one_can_handle_missing_key(self):
        self.request.session = {}
        selected = SelectedPlugins(self.request)
        selected._unselect_one("test")
        self.assertEqual(self.request.session.get("selected"), [])

    def test_unselect_all(self):
        self.request.session.update({"selected": [{"usable_name": "test"}, {"usable_name": "test_02"}]})
        selected = SelectedPlugins(self.request)
        selected._unselect_all()
        self.assertEqual(self.request.session.get("selected"), [])

    @patch("the_elder_commands.utils.selected_plugins.SelectedPlugins._unselect_all")
    @patch("the_elder_commands.utils.selected_plugins.SelectedPlugins._unselect_one")
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

    @patch("the_elder_commands.utils.selected_plugins.SelectedPlugins._unselect_all")
    @patch("the_elder_commands.utils.selected_plugins.SelectedPlugins._unselect_one")
    def test_unselect_for_all(self, one, un_all):
        post = QueryDict("", mutable=True)
        post.update({"unselect": "unselect_all"})
        self.request.session.update({"selected": [{"usable_name": "test"}, {"usable_name": "test_01"}]})
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


class SkillsTest(TestCase):

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
        expected = setup_default_nord()
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
        expected = setup_default_nord()
        actual = default_skills_race_update("nord")
        self.assertDictEqual(actual, expected)


class BaseChosenTest(TestCase):
    class FakeRequest:
        session = {"chosen_key": "Result!"}

    def test_get_return_key_value(self):
        request = self.FakeRequest()
        chosen = BaseChosen(request)
        chosen._key = "chosen_key"
        self.assertEqual(chosen.get(), "Result!")

    def test_if_key_dont_exist_return_empty_dict(self):
        request = self.FakeRequest()
        chosen = BaseChosen(request)
        chosen._key = "chosen_wrong_key"

        self.assertEqual(chosen.get(), {})

    def test_set_value_to_chosen_key(self):
        request = self.FakeRequest()
        chosen = BaseChosen(request)
        chosen._key = "chosen_set_key"
        chosen.set("New value!")
        self.assertEqual(request.session.get("chosen_set_key"), "New value!")


class ConvertValueJSPostTest(TestCase):
    def test_convert_post_to_list_of_form_id_and_amount(self):
        class FakeRequest:
            POST = {"table_input": '[{"name":"0101BFEF","value":"1"},{"name":"010282E9","value":"12"},'
                    '{"name":"010282E6","value":""}]'}

        result = convert_value_post(FakeRequest())
        self.assertEqual(result, {"0101BFEF": "1", "010282E9": "12"})

    def test_missing_table_input_return_empty_dict(self):

        class FakeRequest:
            POST = {}

        request = FakeRequest()
        output = convert_value_post(request)
        self.assertEqual(output, {})


class ConvertValueJSInputTest(TestCase):
    def test_convert_input(self):
        case = [{"value": "1", "name": "A1"}, {"value": "", "name": "A2"}, {"value": "3", "name": "A3"}]
        result = convert_value_input(case)
        expected = {"A1": "1", "A3": "3"}
        self.assertEqual(expected, result)


class CheckRecaptchaTest(TestCase):

    @staticmethod
    @patch("the_elder_commands.utils.check_recaptcha.recaptcha_request")
    @patch("the_elder_commands.utils.check_recaptcha.HttpRequest")
    def make_request(content, http_request_patch, recaptcha_request_patch):
        recaptcha_request_patch.post.return_value = FakeResponse(content)
        http_request_patch.build_absolute_uri.return_value = "url"
        request_data = {"g-recaptcha-response": "response",
                        "secret": settings.RECAPTCHA_SECRET_KEY}

        func = MagicMock()
        request = FakeRequest(request_data)

        check_recaptcha("contact")(func)(request)

        return {"recaptcha_request_patch": recaptcha_request_patch, "function": func, "request": request}

    def test_recaptcha_request_validation(self):
        returns = self.make_request(b'{"success": true, "score": 0.4}')
        recaptcha_request_patch = returns.get("recaptcha_request_patch")
        func = returns.get("function")

        func.assert_called_once()
        recaptcha_request_patch.post.assert_called_once()

        expected_data = {"response": "response",
                         "secret": settings.RECAPTCHA_SECRET_KEY}
        recaptcha_request_patch.post.assert_called_with("https://www.google.com/recaptcha/api/siteverify",
                                                        expected_data)

    def test_recaptcha_run_function_not_called_on_low_score(self):
        returns = self.make_request(b'{"success": true, "score": 0.3}')
        recaptcha_request_patch = returns.get("recaptcha_request_patch")
        func = returns.get("function")

        recaptcha_request_patch.post.assert_called_once()
        func.assert_not_called()

    def test_recaptcha_will_give_message_to_site_on_failure(self):
        returns = self.make_request(b'{"success": true, "score": 0.3}')
        request = returns.get("request")

        message = MessagesSystem(request).pop_contact()
        self.assertEqual(message, ["It looks like you're a bot. If not, contact me the other way. url"])
