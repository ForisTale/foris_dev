from django.test import TestCase
from the_elder_commands.models import Character
from the_elder_commands.services import CharacterService
from the_elder_commands.views import extract_skills, set_skills_values, unpack_post


class CharacterViewTest(TestCase):

    def test_tec_use_template(self):
        response = self.client.get("/the_elder_commands/")
        self.assertTemplateUsed(response, "the_elder_commands/character.html")

    def test_character_view_use_form(self):

        response = self.client.get("/the_elder_commands/")
        self.assertIsInstance(
            response.context["character"],
            CharacterService
        )

    def test_redirect_after_post(self):
        response = self.client.post(
            "/the_elder_commands/",
            data={}
        )
        self.assertRedirects(response, "/the_elder_commands/")

    def test_pass_race_in_url_passed_it_to_form(self):
        self.client.post(
            "/the_elder_commands/",
            data={"race": "Orc"}
        )

        self.assertEqual(Character.objects.count(), 1)
        model = Character.objects.first()
        self.assertEqual(
            model.race,
            "Orc"
        )

    def test_view_build_dict_and_pass_it_to_form(self):
        self.client.post(
            "/the_elder_commands/",
            data={
                "alteration_base": "35",
                "heavyarmor_new": "40",
            }
        )
        model = Character.objects.first()
        self.assertEqual(
            model.default_skills["Magic"]["Alteration"]["value"],
            35
        )
        self.assertEqual(
            model.desired_skills["Combat"]["Heavy Armor"]["value"],
            40
        )


class ExtractSkillsTest(TestCase):

    def test_will_extract_data_from_post(self):
        post = {
            "item": "item",
            "alteration_base": "11",
            "heavyarmor_new": "44",
        }
        extract_skills(post)
        self.assertEqual(post, {"item": "item"})

    def test_return_two_correct_dict(self):
        post = {
            "item": "item",
            "alteration_base": "11",
            "heavyarmor_new": "44",
        }
        default, desired = extract_skills(post)
        self.assertEqual(
            [default, desired],
            [{"alteration": 11}, {"heavyarmor": 44}]
        )


class SetSkillsValuesTest(TestCase):

    def test_will_return_two_correct_dicts(self):
        result_1 = CharacterService.race_skill_update("Nord")
        dictionary = CharacterService.race_skill_update("Nord")
        set_skills_values({"alteration": "45"}, dictionary)
        result_1["Magic"]["Alteration"]["value"] = 45

        self.assertEqual(dictionary, result_1)


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
