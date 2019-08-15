from django.test import TestCase
from the_elder_commands.models import Character
from the_elder_commands.services import CharacterService
from the_elder_commands.inventory import DEFAULT_SKILLS
import copy


class CharacterServiceTest(TestCase):

    @staticmethod
    def set_up_default_nord():
        skills = copy.deepcopy(DEFAULT_SKILLS)
        skills["Combat"]["Two-handed"]["default_value"] += 10
        skills["Stealth"]["Speech"]["default_value"] += 5
        skills["Stealth"]["Light Armor"]["default_value"] += 5
        for skill in ["Block", "One-handed", "Smithing"]:
            skills["Combat"][skill]["default_value"] += 5
        return skills

    @staticmethod
    def set_up_desire_skills():
        skills = CharacterService.default_race_skills_update("Altmer")
        skills["Combat"]["Two-handed"]["desired_value"] = 20
        skills["Stealth"]["Speech"]["desired_value"] = 20
        skills["Stealth"]["Light Armor"]["desired_value"] = 20
        Character.objects.create(race="Altmer", session_key="key", skills=skills)
        character = CharacterService("key")
        return character

    def test_race_skills_update_depend_on_race(self):
        default_skills = CharacterService.default_race_skills_update("Nord")
        skills = self.set_up_default_nord()
        self.assertEqual(default_skills, skills)

    def test_predict_level(self):
        skills = self.set_up_default_nord()
        skills["Combat"]["Archery"]["default_value"] = 20
        skills["Stealth"]["Sneak"]["default_value"] = 20
        skills["Stealth"]["Alchemy"]["default_value"] = 20
        Character.objects.create(session_key="key", skills=skills)
        self.assertEqual(
            CharacterService(session_key="key").default_level,
            3
        )

    def test_commands_list(self):
        character = self.set_up_desire_skills()
        commands_list = [
            "player.advskill twohanded 2525",
            "player.advskill speechcraft 2525",
            "player.advskill lightarmor 2525",
        ]
        self.assertEqual(character.commands_list(), commands_list)

    def test_predict_desired_level_count_from_default(self):
        skills = copy.deepcopy(DEFAULT_SKILLS)
        skills["Magic"]["Alteration"]["default_value"] = 32
        skills["Magic"]["Alteration"]["desired_value"] = 40
        skills["Magic"]["Enchanting"]["default_value"] = 40
        Character.objects.create(session_key="key", skills=skills)
        character = CharacterService(session_key="key")
        self.assertEqual(character.default_level, 7)
        self.assertEqual(character.desired_level, 8)

    def test_if_passes_non_exist_session_key_create_default(self):
        CharacterService(session_key="key")
        character = Character.objects.first()
        self.assertEqual(character.session_key, "key")

    def test_desired_skills_update_return_correct_object(self):
        character = self.set_up_desire_skills()
        self.assertEqual(
            character.skills["Stealth"]["Speech"]["desired_value"],
            20
        )

    def test_empty_character_desired_skills_return_desired_skills_empty_value(self):
        character = CharacterService(session_key="key")
        self.assertEqual(
            character.skills["Magic"]["Alteration"]["desired_value"],
            ""
        )

    def test_desired_level_is_calculated_against_default_skills(self):
        skills = self.set_up_default_nord()
        skills["Combat"]["One-handed"]["default_value"] = 25
        skills["Combat"]["One-handed"]["desired_value"] = 35
        Character.objects.create(session_key="key", skills=skills)
        character = CharacterService(session_key="key")
        self.assertEqual(character.default_level, 2)
        self.assertEqual(character.desired_level, 4)

    def test_calculate_desired_level(self):
        character = self.set_up_desire_skills()
        self.assertEqual(character.desired_level, 3)
        model = Character.objects.get(session_key="key")
        model.desired_level = 6
        model.fill_skills = True
        model.save()
        changed_character = CharacterService(session_key="key")
        self.assertEqual(changed_character.desired_level, 6)

    def test_if_desired_level_is_bigger_than_calculated_then_change_skills(self):
        self.set_up_desire_skills()
        model = Character.objects.get(session_key="key")
        model.desired_level = 6
        model.fill_skills = True
        model.save()
        character = CharacterService(session_key="key")
        cases = [
            character.skills["Combat"]["Archery"]["desired_value"],
            character.skills["Combat"]["Block"]["desired_value"],
            character.skills["Stealth"]["Alchemy"]["desired_value"],
        ]
        for case in cases:
            self.assertNotEqual(case, "")
            self.assertNotEqual(case, 15)

    def test_desired_level_fill_skills_only_to_100(self):
        self.set_up_desire_skills()
        model = Character.objects.get(session_key="key")
        model.desired_level = 81
        model.fill_skills = True
        skills = model.skills
        skills["Magic"]["Alteration"]["desired_value"] = 99
        model.save()

        character = CharacterService(session_key="key")
        self.assertEqual(
            character.skills["Magic"]["Alteration"]["desired_value"],
            100
        )
