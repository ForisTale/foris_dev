from django.test import TestCase
from django.test.utils import tag
from django.http import QueryDict
from the_elder_commands.models import Character, Plugins, PluginVariants
from the_elder_commands.services import CharacterService
from the_elder_commands.views import extract_skills, set_skills_values, unpack_post
from the_elder_commands.inventory import ManageTestFiles, ADD_PLUGIN_SUCCESS_MESSAGE, \
    PLUGIN_TEST_FILE, PLUGIN_TEST_DICT, ADD_PLUGIN_FILE_ERROR_MESSAGE
from unittest.mock import patch

SKILL_POST = {
    'alteration_base': "15",
    'conjuration_base': "15",
    'destruction_base': "15",
    'enchanting_base': "15",
    'illusion_base': "15",
    'restoration_base': "15",
    'marksman_base': "15",
    'block_base': "15",
    'heavyarmor_base': "15",
    'onehanded_base': "15",
    'smithing_base': "15",
    'twohanded_base': "15",
    'alchemy_base': "15",
    'lightarmor_base': "15",
    'lockpicking_base': "15",
    'pickpocket_base': "15",
    'sneak_base': "15",
    'speechcraft_base': "15",
    'alteration_new': "",
    'conjuration_new': "",
    'destruction_new': "",
    'enchanting_new': "",
    'illusion_new': "",
    'restoration_new': "",
    'marksman_new': "",
    'block_new': "",
    'heavyarmor_new': "",
    'onehanded_new': "",
    'smithing_new': "",
    'twohanded_new': "",
    'alchemy_new': "",
    'lightarmor_new': "",
    'lockpicking_new': "",
    'pickpocket_new': "",
    'sneak_new': "",
    'speechcraft_new': "",
}


class CharacterViewTest(TestCase):

    def test_tec_use_template(self):
        response = self.client.get("/the_elder_commands/")
        self.assertTemplateUsed(response, "the_elder_commands/character.html")

    def test_character_view_use_service(self):
        response = self.client.get("/the_elder_commands/")
        self.assertIsInstance(
            response.context["character"],
            CharacterService
        )

    def test_redirect_after_POST(self):
        response = self.client.post(
            "/the_elder_commands/",
            data={}
        )
        self.assertRedirects(response, "/the_elder_commands/")

    def test_pass_race_in_url_passed_it_to_form(self):
        self.client.post("/the_elder_commands/", data={"race": "Ork"})

        self.assertEqual(Character.objects.count(), 1)
        model = Character.objects.first()
        self.assertEqual(
            model.race,
            "Ork"
        )

    def test_view_build_dict_and_pass_it_to_form(self):
        data = SKILL_POST.copy()
        data["alteration_base"] = ["35"]
        data["heavyarmor_new"] = ["40"]

        self.client.post(
            "/the_elder_commands/",
            data=data
        )
        model = Character.objects.first()
        self.assertEqual(
            model.skills["Magic"]["Alteration"]["default_value"],
            35
        )
        self.assertEqual(
            model.skills["Combat"]["Heavy Armor"]["desired_value"],
            40
        )
        self.assertEqual(
            model.skills["Magic"]["Alteration"]["desired_value"],
            ""
        )

    def test_after_send_POST_character_give_correct_level(self):
        self.client.post("/the_elder_commands/", data={"race": "Ork"})
        data = SKILL_POST.copy()
        data["twohanded_new"] = ["21"]
        data["speechcraft_new"] = ["21"]
        data["lightarmor_new"] = ["21"]
        self.client.post(
            "/the_elder_commands/",
            data=data
        )

        key = Character.objects.first().session_key
        character = CharacterService(session_key=key)
        self.assertEqual(
            character.desired_level,
            3
        )


class ItemsViewTest(TestCase):

    def test_items_use_template(self):
        response = self.client.get("/the_elder_commands/items/")
        self.assertTemplateUsed(response, "the_elder_commands/items.html")


class PluginsViewTest(TestCase, ManageTestFiles):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ManageTestFiles.__init__(self)

    def setUp(self):
        super().setUp()

        if self.check_test_tag("create_test_file"):
            self.create_test_files({"TEC_test_file.tec": PLUGIN_TEST_FILE})
        elif self.check_test_tag("create_incorrect_file"):
            self.create_test_files({"TEC_test_file.ini": {"test": 1}})

    def tearDown(self):
        self.delete_test_files()
        super().tearDown()

    def send_default_post_and_return_response(self):
        with open(self.test_files_full_path[0], "r", encoding="utf-8") as file:
            data = {
                "plugin_name": ["test 01'5<>(){}[]a'n\"*"],
                "plugin_version": ["0.1"],
                "plugin_language": ["Polish"],
                "plugin_file": file,
            }
            return self.client.post("/the_elder_commands/plugins/", data=data)

    def test_plugins_use_template(self):
        response = self.client.get("/the_elder_commands/plugins/")
        self.assertTemplateUsed(response, "the_elder_commands/plugins.html")

    @tag("create_test_file")
    def test_view_pass_plugins(self):
        self.send_default_post_and_return_response()
        response = self.client.get("/the_elder_commands/plugins/")
        self.assertEqual(
            "test 015an",
            response.context["plugins"][0].get("name", "")
        )

    @tag("create_test_file")
    def test_view_pass_messages(self):
        response = self.client.get("/the_elder_commands/plugins/")
        self.assertEqual(
            response.context.get("add_plugin_messages"),
            []
        )
        self.send_default_post_and_return_response()
        response = self.client.get("/the_elder_commands/plugins/")
        self.assertEqual(
            response.context["add_plugin_messages"],
            [ADD_PLUGIN_SUCCESS_MESSAGE]
        )

    @tag("create_incorrect_file")
    def test_view_show_error_message(self):
        response = self.send_default_post_and_return_response()
        self.client.get("/the_elder_commands/plugins/")
        self.assertEqual(
            response.context["add_plugin_messages"],
            [ADD_PLUGIN_FILE_ERROR_MESSAGE]
        )

    @tag("create_test_file")
    def test_success_message_dont_show_after_reload(self):
        self.send_default_post_and_return_response()
        self.client.get("/the_elder_commands/plugins/")
        response = self.client.get("/the_elder_commands/plugins/")
        self.assertEqual(
            response.context["add_plugin_messages"],
            []
        )

    @tag("create_test_file")
    def test_plugins_redirect_after_POST(self):
        response = self.send_default_post_and_return_response()
        self.assertRedirects(response, "/the_elder_commands/plugins/")

    @tag("create_test_file")
    def test_pass_POST_to_model(self):
        self.send_default_post_and_return_response()

        plugin_model = Plugins.objects.first()
        variants_model = PluginVariants.objects.first()

        plugin_cases = {
            "name": "test 015an",
            "usable_name": "test_015an",
            }
        for field, desired_result in plugin_cases.items():
            self.assertEqual(
                plugin_model.__getattribute__(field),
                desired_result
            )

        variants_cases = {
            "version": "0.1",
            "language": "Polish",
            "plugin_data": PLUGIN_TEST_DICT,
        }
        for field, desired_result in variants_cases.items():
            self.assertEqual(
                variants_model.__getattribute__(field),
                desired_result
            )

    @tag("create_test_file")
    @patch("the_elder_commands.views.PluginVariantsForm")
    def test_file_is_changed_to_dict_before_pass_POST_to_form(self, form_mock):
        self.send_default_post_and_return_response()

        expected = QueryDict("", mutable=True)
        plugin = Plugins.objects.first()
        expected.update({
            'version': '0.1', 'language': 'Polish', 'plugin_data': PLUGIN_TEST_DICT
        })
        form_mock.assert_called_once()
        form_mock.assert_called_with(data=expected, instance=plugin)


class ExtractSkillsTest(TestCase):

    def test_will_extract_data_from_POST(self):
        post = {
            "item": "item",
            "alteration_base": "11",
            "heavyarmor_new": "44",
            "alteration_multiplier": "on"
        }
        extract_skills(post)
        self.assertEqual(post, {"item": "item"})

    def test_return_two_correct_dict(self):
        post = {
            "item": "item",
            "alteration_base": "11",
            "heavyarmor_new": "44",
            "alteration_multiplier": "on",
        }
        skills = extract_skills(post)
        self.assertEqual(
            skills,
            {"default": {"alteration": "11"},
             "desired": {"heavyarmor": "44"},
             "multiplier": {"alteration": True}}
        )


class SetSkillsValuesTest(TestCase):

    def test_will_return_two_correct_dicts(self):
        result = CharacterService.default_race_skills_update("Nord")
        dictionary = CharacterService.default_race_skills_update("Nord")
        set_skills_values({"default": {"alteration": "45"}, "priority": {"alteration": True}}, dictionary)
        result["Magic"]["Alteration"]["default_value"] = "45"
        result["Magic"]["Alteration"]["multiplier"] = True

        self.assertEqual(dictionary, result)

    def test_empty_value_is_set_as_none(self):
        result = CharacterService.default_race_skills_update("Nord")
        dictionary = CharacterService.default_race_skills_update("Nord")
        set_skills_values({"desired": {"heavyarmor": ""}}, dictionary)
        result["Magic"]["Alteration"]["desired_value"] = ""
        self.assertEqual(result, dictionary)


class UnpackPOSTTest(TestCase):

    def test_return_correct_dict(self):
        post = {
            "item": ["item"],
            "other_item": ["other"],
            "multi_items": ["one", "two"],
        }
        result = unpack_post(post)
        expected = {
            "item": "item",
            "other_item": "other",
            "multi_items": ["one", "two"],
        }
        self.assertEqual(result, expected)
