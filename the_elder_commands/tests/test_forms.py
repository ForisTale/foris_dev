from django.test import TestCase
from the_elder_commands.forms import CharacterForm, PluginsForm
from the_elder_commands.models import Character, Plugins
from the_elder_commands.services import CharacterService


class CharacterFormTest(TestCase):

    def test_form_passes_data_to_model(self):
        instance = Character.objects.get_or_create(session_key="key")[0]
        form = CharacterForm(data={"race": "Nord"}, instance=instance)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Character.objects.count(), 1)
        self.assertEqual(
            Character.objects.get(session_key="key"),
            Character.objects.all()[0]
        )


class CharacterFormValidationTest(TestCase):
    def setUp(self):
        self.instance = Character.objects.get_or_create(session_key="key")[0]

    def check_fail_and_message(self, form, error_message):
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            error_message
        )

    def test_desired_level_range(self):
        cases = [0, 82, -20]
        for case in cases:
            form = CharacterForm(data={"desired_level": str(case)}, instance=self.instance)
            self.check_fail_and_message(form, {"desired_level":
                                               ["The desired level need to be a integer between 1 and 81."]})
        form = CharacterForm(data={"desired_level": 5}, instance=self.instance)
        self.assertTrue(form.is_valid())

    def test_desired_level_is_number(self):
        form = CharacterForm(data={"desired_level": "ala"}, instance=self.instance)
        self.check_fail_and_message(form, {"desired_level":
                                           ["Enter a whole number."]})

    def test_priority_multiplier_is_number(self):
        form = CharacterForm(data={"priority_multiplier": "ala"}, instance=self.instance)
        self.check_fail_and_message(form, {'priority_multiplier': ['Enter a number.']})

    def test_skills_range(self):
        skills = CharacterService.default_race_skills_update("Nord")
        cases = ["14", "101", "-50"]
        for kind in ["default", "desired"]:
            for case in cases:
                skills["Magic"]["Alteration"][kind + "_value"] = case
                form = CharacterForm(data={"skills": skills}, instance=self.instance)
                self.check_fail_and_message(form, {'skills':
                                                   ['The skill need to be a integer between 15 and 100.']})
            skills["Magic"]["Alteration"][kind + "_value"] = "15"
            form = CharacterForm(data={"skills": skills}, instance=self.instance)
            self.assertTrue(form.is_valid())

    def test_skills_values_are_numbers(self):
        skills = CharacterService.default_race_skills_update("Nord")
        skills["Magic"]["Alteration"]["default_value"] = "test"
        skills["Magic"]["Alteration"]["desired_value"] = "test"
        form = CharacterForm(data={"skills": skills}, instance=self.instance)
        self.check_fail_and_message(form, {"skills":
                                           ['All skills values must be integers!']})

    def test_desired_must_be_bigger_than_default(self):
        skills = CharacterService.default_race_skills_update("Nord")
        skills["Magic"]["Alteration"]["default_value"] = 55
        skills["Magic"]["Alteration"]["desired_value"] = 35
        form = CharacterForm(data={"skills": skills}, instance=self.instance)
        self.check_fail_and_message(form, {'skills': ['New value of skills must be bigger than a value!']})

        skills["Magic"]["Alteration"]["desired_value"] = 56
        form = CharacterForm(data={"skills": skills}, instance=self.instance)
        self.assertTrue(form.is_valid())


class PluginsFormTest(TestCase):

    def test_form_pass_data_to_model(self):
        data = {
            "plugin_name": ["test_01"],
            "plugin_version": ["0.1"],
            "plugin_language": ["Polish"],
            "plugin_data": {"test": 1},
        }
        form = PluginsForm(data=data)

        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Plugins.objects.count(), 1)
        self.assertEqual(
            Plugins.objects.get(plugin_name=["test_01"]),
            Plugins.objects.all()[0]
        )
