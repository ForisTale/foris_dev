from .models import Character
from .inventory import PLAYABLE_RACES, DEFAULT_SKILLS, RACES_EXTRA_SKILLS
import copy
import math


class CharacterService:
    def __init__(self, session_key):
        character, created = Character.objects.get_or_create(session_key=session_key)

        self.playable_races = PLAYABLE_RACES
        self.race = character.race
        if not character.skills:
            self.skills = self.default_race_skills_update(character.race)
        else:
            self.skills = character.skills
        self.default_level = self.predict_level(self.default_race_skills_update(self.race), "default")
        self.desired_level = self.predict_level(self.default_race_skills_update(self.race), "desired")

    @staticmethod
    def default_race_skills_update(race):
        skills_tree = copy.deepcopy(DEFAULT_SKILLS)
        for category, skills in RACES_EXTRA_SKILLS[race][10].items():
            skills_tree[category][skills]["default_value"] += 10
        for category, skills in RACES_EXTRA_SKILLS[race][5].items():
            for skill in skills:
                skills_tree[category][skill]["default_value"] += 5
        return skills_tree

    def predict_level(self, base, kind):
        default = base
        total_exp = 0
        for category, skills in self.skills.items():
            for name, skill in skills.items():
                if skill["desired_value"] == "":
                    continue
                default_value = default[category][name]["default_value"]
                if skill[kind + "_value"] > default_value:
                    for char_xp in range(default_value + 1, skill[kind + "_value"] + 1):
                        total_exp += char_xp
        level = (-2.5 + math.sqrt(8 * total_exp + 1225) / 10)
        return int(level)

    def skills_for_desired_level(self):
        skills_base = {}
        for category, skills in self.skills.items():
            skills_base[category] = {}
            for name, skill in skills.items():
                skills_base[category][name] = {}
                desired_value = self.skills[category][name]["value"]
                default_value = skill["value"]
                if desired_value == "":
                    skills_base[category][name]["value"] = default_value
                if desired_value:
                    skills_base[category][name]["value"] = desired_value
        return skills_base

    def commands_list(self):
        total_exp = 0
        commands = []
        for category, skills in self.skills.items():
            for name, skill in skills.items():
                if skill["desired_value"] == "":
                    continue
                default_value = skill["default_value"]
                if skill["desired_value"] > default_value:
                    for skill_level in range(default_value, skill["desired_value"]):
                        total_exp += skill["sim"] * (skill_level ** 1.95) + skill["sio"]
                    commands.append(f"player.advskill {skill['console_name']} {int(total_exp) + 1}")
                    total_exp = 0
        return commands
