import math

from the_elder_commands.utils.defauld_skills_race_update import default_skills_race_update
from the_elder_commands.utils.skills import Skills


class SkillsService:
    def __init__(self, request):
        skills = Skills(request)
        self.race = skills.get_race()
        self.skills = skills.get_skills()
        self.multiplier = skills.get_multiplier()
        self.fill_skills = skills.get_fill_skills()
        self.default_level = self.predict_level("default")
        self.desired_level = self.predict_desired_level(request)
        self.commands = self.commands_list()

    def predict_level(self, kind):
        default = default_skills_race_update(self.race)
        total_exp = 0
        for category, skills in self.skills.items():
            for name, skill in skills.items():
                default_value = default[category][name]["default_value"]
                if skill.get("desired_value") == "" and kind == "desired":
                    for char_xp in range(default_value + 1, skill.get("default_value") + 1):
                        total_exp += char_xp
                    continue
                if skill[kind + "_value"] > default_value:
                    for char_xp in range(default_value + 1, skill[kind + "_value"] + 1):
                        total_exp += char_xp
        level = (-2.5 + math.sqrt(8 * total_exp + 1225) / 10)
        return int(level)

    def predict_desired_level(self, request):
        skill = Skills(request)
        target_level = skill.get_desired_level()
        if self.default_level < target_level and self.fill_skills:
            self.set_skills_to_desired_level(target_level)
            return target_level
        else:
            return self.predict_level("desired")

    def set_skills_to_desired_level(self, target_level):
        total_exp = self.count_needed_exp(target_level)
        values = {}
        while total_exp > 0:
            all_skills_filled = 0
            for category, skills in self.skills.items():
                for skill_name, skill in skills.items():
                    # noinspection PyUnresolvedReferences
                    value = values.get(skill_name, 1)
                    while value >= 1:
                        if skill.get("desired_value") == 100:
                            all_skills_filled += 1
                            break
                        if skill.get("desired_value") == "":
                            skill.update({"desired_value": skill.get("default_value") + 1})
                        else:
                            skill.update({"desired_value": skill.get("desired_value") + 1})
                        total_exp -= skill.get("desired_value")
                        value -= 1
                    if skill.get("multiplier"):
                        value += self.multiplier
                    else:
                        value += 1
                    values.update({skill_name: value})
            if all_skills_filled == 18:
                break

    def count_needed_exp(self, target_level):
        predicted_level = self.predict_level("desired")
        predicted_exp = 12.5 * (predicted_level ** 2) + 62.5 * predicted_level - 75
        target_exp = 12.5 * (target_level ** 2) + 62.5 * target_level - 75
        total_exp = target_exp - predicted_exp
        return total_exp

    def commands_list(self):
        total_exp = 0
        commands = []
        for skills in self.skills.values():
            for name, skill in skills.items():
                if skill["desired_value"] == "":
                    continue
                default_value = skill.get("default_value")
                if skill["desired_value"] > default_value:
                    for skill_level in range(default_value, skill.get("desired_value")):
                        skill_xp = skill.get("sim") * (skill_level ** 1.95) + skill.get("sio")
                        total_exp += skill_xp
                    skill_command_value = total_exp / skill.get("sum")
                    total_exp = 0
                    commands.append(f"player.advskill {skill['console_name']} {int(skill_command_value) + 1}")
        return commands