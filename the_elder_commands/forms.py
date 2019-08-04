from functional_tests.the_elder_commands.test_character import DEFAULT_SKILL
import copy


class CharacterForm:
    def __init__(self, race=None):
        self.skills = None
        self.race = race
        self.race_skill_update(race)

    def race_skill_update(self, race):
        skills = copy.deepcopy(DEFAULT_SKILL)

        if race == "Nord":
            skills["Combat"]["Two-handed"] += 10
            skills["Stealth"]["Speech"] += 5
            skills["Stealth"]["Light Armor"] += 5
            for skill in ["Block", "One-handed", "Smithing"]:
                skills["Combat"][skill] += 5

        self.skills = skills
