from django.test import TestCase

from the_elder_commands.models import Skills
from the_elder_commands.services import SkillsService
from the_elder_commands.views import extract_skills, set_skills_values, unpack_post
from the_elder_commands.inventory import SKILL_POST, SKILLS_ERROR_VALUES_MUST_BE_INTEGERS


class SkillsViewTest(TestCase):
    base_url = "/the_elder_commands/skills/"

    def test_tec_use_template(self):
        response = self.client.get(self.base_url)
        self.assertTemplateUsed(response, "the_elder_commands/skills.html")

    def test_default_url_connect_to_correct_template(self):
        response = self.client.get("/the_elder_commands/")
        self.assertTemplateUsed(response, "the_elder_commands/skills.html")

    def test_character_view_use_service(self):
        response = self.client.get(self.base_url)
        self.assertIsInstance(response.context["service"], SkillsService)

    def test_redirect_after_POST(self):
        response = self.client.post(self.base_url, data={})
        self.assertRedirects(response, self.base_url)

    def test_pass_race_in_url_passed_it_to_form(self):
        self.client.post(self.base_url, data={"race": "Ork"})

        self.assertEqual(Skills.objects.count(), 1)
        model = Skills.objects.first()
        self.assertEqual(model.race, "Ork")

    def test_view_build_dict_and_pass_it_to_form(self):
        data = SKILL_POST.copy()
        data["alteration_base"] = ["35"]
        data["heavyarmor_new"] = ["40"]

        self.client.post(self.base_url, data=data)
        model = Skills.objects.first()
        self.assertEqual(model.skills["Magic"]["Alteration"]["default_value"], 35)
        self.assertEqual(model.skills["Combat"]["Heavy Armor"]["desired_value"], 40)
        self.assertEqual(model.skills["Magic"]["Alteration"]["desired_value"], "")

    def test_after_send_POST_character_give_correct_level(self):
        self.client.post(self.base_url, data={"race": "Ork"})
        data = SKILL_POST.copy()
        data["twohanded_new"] = ["21"]
        data["speechcraft_new"] = ["21"]
        data["lightarmor_new"] = ["21"]
        self.client.post(self.base_url, data=data)

        key = Skills.objects.first().session_key
        character = SkillsService(session_key=key)
        self.assertEqual(character.desired_level, 3)

    def test_skill_view_pass_correct_error(self):
        data = SKILL_POST.copy()
        data.update({"alteration_base": ""})
        self.client.post(self.base_url, data=data)
        response = self.client.get(self.base_url)
        self.assertEqual(response.context["skills_messages"], [SKILLS_ERROR_VALUES_MUST_BE_INTEGERS])

    def test_change_race_dont_give_message(self):
        self.client.post(self.base_url, data={"race": "Ork"})
        response = self.client.get(self.base_url)
        self.assertEqual(response.context["skills_messages"], [])


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
