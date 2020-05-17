from django.test import TestCase

from the_elder_commands.models import Skills
from the_elder_commands.services import SkillsService
from the_elder_commands.views import extract_skills, set_skills_values, unpack_post

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


class SkillsViewTest(TestCase):

    def test_tec_use_template(self):
        response = self.client.get("/the_elder_commands/")
        self.assertTemplateUsed(response, "the_elder_commands/skills.html")

    def test_character_view_use_service(self):
        response = self.client.get("/the_elder_commands/")
        self.assertIsInstance(
            response.context["service"],
            SkillsService
        )

    def test_redirect_after_POST(self):
        response = self.client.post(
            "/the_elder_commands/",
            data={}
        )
        self.assertRedirects(response, "/the_elder_commands/")

    def test_pass_race_in_url_passed_it_to_form(self):
        self.client.post("/the_elder_commands/", data={"race": "Ork"})

        self.assertEqual(Skills.objects.count(), 1)
        model = Skills.objects.first()
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
        model = Skills.objects.first()
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

        key = Skills.objects.first().session_key
        character = SkillsService(session_key=key)
        self.assertEqual(
            character.desired_level,
            3
        )


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
        result = SkillsService.default_race_skills_update("Nord")
        dictionary = SkillsService.default_race_skills_update("Nord")
        set_skills_values({"default": {"alteration": "45"}, "priority": {"alteration": True}}, dictionary)
        result["Magic"]["Alteration"]["default_value"] = "45"
        result["Magic"]["Alteration"]["multiplier"] = True

        self.assertEqual(dictionary, result)

    def test_empty_value_is_set_as_none(self):
        result = SkillsService.default_race_skills_update("Nord")
        dictionary = SkillsService.default_race_skills_update("Nord")
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
