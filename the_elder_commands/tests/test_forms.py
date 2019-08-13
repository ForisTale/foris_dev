from django.test import TestCase
from the_elder_commands.forms import CharacterForm
from the_elder_commands.models import Character
from the_elder_commands.services import CharacterService


class CharacterFormTest(TestCase):

    def test_form_passes_data_to_service(self):
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

    def test_default_skills_range(self):
        default_skills = CharacterService.default_race_skills_update("Nord")
        cases = ["14", "101", "-50"]
        for case in cases:
            default_skills["Magic"]["Alteration"]["value"] = case
            form = CharacterForm(data={"default_skills": default_skills}, instance=self.instance)
            self.check_fail_and_message(form, {'default_skills':
                                               ['The skill need to be a integer between 15 and 100.']})
        default_skills["Magic"]["Alteration"]["value"] = "15"
        form = CharacterForm(data={"default_skills": default_skills}, instance=self.instance)
        self.assertTrue(form.is_valid())

    def test_desired_skills_range(self):
        desired_skills = CharacterService.default_race_skills_update("Nord")
        cases = ["14", "101", "-50"]
        for case in cases:
            desired_skills["Magic"]["Alteration"]["value"] = case
            form = CharacterForm(data={"desired_skills": desired_skills}, instance=self.instance)
            self.check_fail_and_message(form, {'desired_skills':
                                               ['The skill need to be a integer between 15 and 100.']})
        desired_skills["Magic"]["Alteration"]["value"] = "15"
        form = CharacterForm(data={"desired_skills": desired_skills}, instance=self.instance)
        self.assertTrue(form.is_valid())

    def test_skills_values_are_numbers(self):
        default_skills = CharacterService.default_race_skills_update("Nord")
        desired_skills = CharacterService.default_race_skills_update("Nord")
        default_skills["Magic"]["Alteration"]["value"] = "test"
        desired_skills["Magic"]["Alteration"]["value"] = "test"
        for case in [[{"default_skills": default_skills}, "default_skills"],
                     [{"desired_skills": desired_skills}, "desired_skills"]]:
            form = CharacterForm(data=case[0], instance=self.instance)
            self.check_fail_and_message(form, {case[1]:
                                               ['All skills values must be integers!']})

    def test_desired_must_be_bigger_than_default(self):
        default_skills = CharacterService.default_race_skills_update("Nord")
        desired_skills = CharacterService.default_race_skills_update("Nord")
        default_skills["Magic"]["Alteration"]["value"] = 55
        form = CharacterForm(data={"default_skills": default_skills, "desired_skills": desired_skills},
                             instance=self.instance)
        self.check_fail_and_message(form, {'__all__': ['New value of skills must be bigger than a value!']})

        desired_skills["Magic"]["Alteration"]["value"] = 56
        form = CharacterForm(data={"default_skills": default_skills, "desired_skills": desired_skills},
                             instance=self.instance)
        self.assertTrue(form.is_valid())
