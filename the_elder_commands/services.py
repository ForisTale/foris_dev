from .models import Character
from .inventory import DEFAULT_SKILLS, RACES_EXTRA_SKILLS
import copy
import math


class CharacterService:
    def __init__(self, session_key):
        character, created = Character.objects.get_or_create(session_key=session_key)

        self.race = character.race
        if not character.skills:
            self.skills = self.default_race_skills_update(race=character.race)
        else:
            self.skills = character.skills
        self.priority_multiplier = character.priority_multiplier
        self.fill_skills = character.fill_skills
        self.desired_level = self.predict_desired_level(character_model=character)
        self.default_level = self.predict_level("default")
        self.list_of_character_commands = self.commands_list()

    @staticmethod
    def default_race_skills_update(race):
        skills_tree = copy.deepcopy(DEFAULT_SKILLS)
        for category, skills in RACES_EXTRA_SKILLS[race][10].items():
            skills_tree[category][skills]["default_value"] += 10
        for category, skills in RACES_EXTRA_SKILLS[race][5].items():
            for skill in skills:
                skills_tree[category][skill]["default_value"] += 5
        return skills_tree

    def predict_level(self, kind):
        default = self.default_race_skills_update(self.race)
        total_exp = 0
        for category, skills in self.skills.items():
            for name, skill in skills.items():
                default_value = default[category][name]["default_value"]
                if skill["desired_value"] == "" and kind == "desired":
                    for char_xp in range(default_value + 1, skill["default_value"] + 1):
                        total_exp += char_xp
                    continue
                if skill[kind + "_value"] > default_value:
                    for char_xp in range(default_value + 1, skill[kind + "_value"] + 1):
                        total_exp += char_xp
        level = (-2.5 + math.sqrt(8 * total_exp + 1225) / 10)
        return int(level)

    def predict_desired_level(self, character_model):
        predicted_level = self.predict_level("desired")
        target_level = character_model.desired_level
        if target_level <= predicted_level:
            return predicted_level
        elif not character_model.fill_skills:
            return predicted_level
        else:
            return self.set_skills_to_desired_level(character_model)

    def set_skills_to_desired_level(self, character_model):
        total_exp = self.count_needed_exp(character_model)
        all_skills = self.create_multiplier_skill_template(character_model)
        while total_exp > 0:
            for category, skills in all_skills.items():
                for skill_name in skills.keys():
                    skill = self.skills[category][skill_name]
                    while all_skills[category][skill_name]["value"] >= 1:
                        if skill["desired_value"] == 100:
                            break
                        if skill["desired_value"] == "":
                            skill["desired_value"] = skill["default_value"] + 1
                        else:
                            skill["desired_value"] = skill["desired_value"] + 1
                        total_exp -= skill["desired_value"]
                        all_skills[category][skill_name]["value"] -= 1
                    all_skills[category][skill_name]["value"] += all_skills[category][skill_name]["multiplier"]
        return character_model.desired_level

    def create_multiplier_skill_template(self, character_model):
        all_skills = {}
        for category, skills in self.skills.items():
            all_skills[category] = {}
            for skill_name, skill in skills.items():
                all_skills[category][skill_name] = {}
                if skill["multiplier"]:
                    all_skills[category][skill_name]["multiplier"] = character_model.priority_multiplier
                    all_skills[category][skill_name]["value"] = character_model.priority_multiplier
                else:
                    all_skills[category][skill_name]["multiplier"] = 1
                    all_skills[category][skill_name]["value"] = 1
        return all_skills

    def count_needed_exp(self, character_model):
        predicted_level = self.predict_level("desired")
        target_level = character_model.desired_level
        predicted_exp = 12.5 * (predicted_level ** 2) + 62.5 * predicted_level - 75
        target_exp = 12.5 * (target_level ** 2) + 62.5 * target_level - 75
        total_exp = target_exp - predicted_exp
        return total_exp

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
                        skill_xp = skill["sim"] * (skill_level ** 1.95) + skill["sio"]
                        total_exp += skill_xp
                    skill_command_value = total_exp / skill["sum"]
                    total_exp = 0
                    commands.append(f"player.advskill {skill['console_name']} {int(skill_command_value) + 1}")
        return commands
