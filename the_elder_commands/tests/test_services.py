from django.test import TestCase
from the_elder_commands.models import Character
from the_elder_commands.services import CharacterService
from the_elder_commands.inventory import DEFAULT_SKILLS, PLAYABLE_RACES
import copy


class CharacterServiceTest(TestCase):

    @staticmethod
    def set_up_default_nord():
        skills = copy.deepcopy(DEFAULT_SKILLS)
        skills["Combat"]["Two-handed"]["value"] += 10
        skills["Stealth"]["Speech"]["value"] += 5
        skills["Stealth"]["Light Armor"]["value"] += 5
        for skill in ["Block", "One-handed", "Smithing"]:
            skills["Combat"][skill]["value"] += 5
        return skills

    @staticmethod
    def set_up_desire_skills():
        Character.objects.create(race="Altmer", session_key="key")
        character = CharacterService("key")
        character.desired_skills["Combat"]["Two-handed"]["value"] = 20
        character.desired_skills["Stealth"]["Speech"]["value"] = 20
        character.desired_skills["Stealth"]["Light Armor"]["value"] = 20
        return character

    def test_can_be_used_to_pass_data(self):
        Character.objects.create(session_key="key")
        default_race = CharacterService(session_key="key")
        self.assertEqual(default_race.race, "Nord")

        Character.objects.create(race="Ork", session_key="ork")
        ork_race = CharacterService(session_key="ork")
        self.assertEqual(ork_race.race, "Ork")

    def test_can_pass_playable_races(self):
        Character.objects.create(session_key="key")
        self.assertEqual(
            CharacterService(session_key="key").playable_races,
            PLAYABLE_RACES
        )

    def test_can_pass_race(self):
        Character.objects.create(race="Altmer", session_key="key")
        self.assertEqual(CharacterService(session_key="key").race, "Altmer")

    def test_race_skills_update_depend_on_race(self):
        default_skills = CharacterService.default_race_skills_update("Nord")
        skills = self.set_up_default_nord()
        self.assertEqual(default_skills, skills)

    def test_predict_level(self):
        character = self.set_up_desire_skills()
        level = character.predict_level(
            character.default_race_skills_update(character.race),
            character.desired_skills
        )
        self.assertEqual(level, 3)

    def test_commands_list(self):
        character = self.set_up_desire_skills()
        commands_list = [
            "player.advskill twohanded 2525",
            "player.advskill lightarmor 2525",
            "player.advskill speechcraft 2525",
        ]
        self.assertEqual(character.commands_list(), commands_list)

    def test_if_passes_non_exist_session_key_create_default(self):
        CharacterService(session_key="key")
        character = Character.objects.first()

        self.assertEqual(character.session_key, "key")

    def test_desired_skills_update_return_correct_object(self):
        character = self.set_up_desire_skills()
        self.assertEqual(
            character.desired_skills["Stealth"]["Speech"]["value"],
            20
        )

    def test_empty_character_desired_skills_return_desired_skills_empty_value(self):
        character = CharacterService(session_key="key")
        self.assertEqual(
            character.desired_skills["Magic"]["Alteration"]["value"],
            ""
        )

    def test_desired_level_is_calculated_against_default_skills(self):
        skills = self.set_up_default_nord()
        skills["Combat"]["One-handed"]["value"] = 35
        Character.objects.create(session_key="key", default_skills=skills)
        character = CharacterService(session_key="key")
        self.assertEqual(character.desired_level, 4)
