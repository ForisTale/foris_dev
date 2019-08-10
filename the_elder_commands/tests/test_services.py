from django.test import TestCase
from the_elder_commands.models import Character
from the_elder_commands.services import CharacterService
from the_elder_commands.inventory import DEFAULT_SKILLS, PLAYABLE_RACES
import copy


class CharacterServiceTest(TestCase):

    @staticmethod
    def default_nord():
        skills = copy.deepcopy(DEFAULT_SKILLS)
        skills["Combat"]["Two-handed"]["value"] += 10
        skills["Stealth"]["Speech"]["value"] += 5
        skills["Stealth"]["Light Armor"]["value"] += 5
        for skill in ["Block", "One-handed", "Smithing"]:
            skills["Combat"][skill]["value"] += 5
        return skills

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

    def test_skills_value_depend_on_race(self):
        Character.objects.create(race="Nord", session_key="key")
        skills = self.default_nord()
        self.assertEqual(CharacterService(session_key="key").default_skills, skills)

    def test_predict_level_and_commands_list(self):
        Character.objects.create(race="Altmer", session_key="key")
        character = CharacterService("key")
        character.desired_skills = copy.deepcopy(DEFAULT_SKILLS)
        character.desired_skills["Combat"]["Two-handed"]["value"] += 5
        character.desired_skills["Stealth"]["Speech"]["value"] += 5
        character.desired_skills["Stealth"]["Light Armor"]["value"] += 5

        self.assertEqual(character.predict_level, 3)
        commands_list = [
            "player.advskill twohanded 2865",
            "player.advskill speech 2865",
            "player.advskill lightarmor 2865",
        ]
        self.assertEqual(character.commands_list, commands_list)

    def test_if_passes_non_exist_session_key_create_default(self):
        character = CharacterService(session_key="key")

        self.assertEqual(character.race, "Nord")
        self.assertEqual(character.default_skills, self.default_nord())
