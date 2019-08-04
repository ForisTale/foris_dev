from django.test import TestCase
from the_elder_commands.forms import CharacterForm
from functional_tests.the_elder_commands.test_character import DEFAULT_SKILL
import copy


class CharacterFormTest(TestCase):

    def test_character_form_skills_value_depend_on_race(self):
        form = CharacterForm()
        self.assertEqual(form.skills, DEFAULT_SKILL)

        nord_form = CharacterForm("Nord")
        skills = copy.deepcopy(DEFAULT_SKILL)
        skills["Combat"]["Two-handed"] += 10
        skills["Stealth"]["Speech"] += 5
        skills["Stealth"]["Light Armor"] += 5
        for skill in ["Block", "One-handed", "Smithing"]:
            skills["Combat"][skill] += 5
        self.assertEqual(nord_form.skills, skills)
