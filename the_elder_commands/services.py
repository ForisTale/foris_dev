from .models import Character
from .inventory import PLAYABLE_RACES, DEFAULT_SKILLS, RACES_EXTRA_SKILLS
import copy
import math


class CharacterService:
    def __init__(self, session_key):
        character, created = Character.objects.get_or_create(session_key=session_key)

        self.playable_races = PLAYABLE_RACES
        self.race = character.race
        if not character.default_skills:
            self.default_skills = self.default_race_skills_update(character.race)
        else:
            self.default_skills = character.default_skills
        self.desired_skills = self.desired_skills_update(character)
        self.default_level = self.predict_level(self.default_race_skills_update(self.race), self.default_skills)
        self.desired_level = self.predict_level(self.default_race_skills_update(self.race),
                                                self.skills_for_desired_level())

    @staticmethod
    def default_race_skills_update(race):
        skills_tree = copy.deepcopy(DEFAULT_SKILLS)
        for category, skills in RACES_EXTRA_SKILLS[race][10].items():
            skills_tree[category][skills]["value"] += 10
        for category, skills in RACES_EXTRA_SKILLS[race][5].items():
            for skill in skills:
                skills_tree[category][skill]["value"] += 5
        return skills_tree

    def desired_skills_update(self, character):
        if character.desired_skills:
            return character.desired_skills

        desired_skills = copy.deepcopy(self.default_skills)
        for skills in desired_skills.values():
            for skill in skills.values():
                skill["value"] = ""
        return desired_skills

    @staticmethod
    def predict_level(base, check_against):
        default = base
        total_exp = 0
        for category, skills in check_against.items():
            for name, skill in skills.items():
                if skill["value"] == "":
                    continue
                default_value = default[category][name]["value"]
                if skill["value"] > default_value:
                    for char_xp in range(default_value + 1, skill["value"] + 1):
                        total_exp += char_xp
        level = (-2.5 + math.sqrt(8 * total_exp + 1225) / 10)
        return int(level)

    def skills_for_desired_level(self):
        skills_base = {}
        for category, skills in self.default_skills.items():
            skills_base[category] = {}
            for name, skill in skills.items():
                skills_base[category][name] = {}
                desired_value = self.desired_skills[category][name]["value"]
                default_value = skill["value"]
                if desired_value == "":
                    skills_base[category][name]["value"] = default_value
                if desired_value:
                    skills_base[category][name]["value"] = desired_value
        return skills_base

    def commands_list(self):
        total_exp = 0
        commands = []
        for category, skills in self.desired_skills.items():
            for name, skill in skills.items():
                if skill["value"] == "":
                    continue
                default_value = self.default_skills[category][name]["value"]
                if skill["value"] > default_value:
                    for skill_level in range(default_value, skill["value"]):
                        total_exp += skill["sim"] * (skill_level ** 1.95) + skill["sio"]
                    commands.append(f"player.advskill {skill['console_name']} {int(total_exp) + 1}")
                    total_exp = 0
        return commands
