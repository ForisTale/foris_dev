import copy

from the_elder_commands.inventory import SKILLS_ERROR_DESIRED_LEVEL_RANGE, SKILLS_ERROR_DESIRED_LEVEL, \
    SKILLS_ERROR_MULTIPLIER, DEFAULT_SKILLS, SKILLS_ERROR_NEW_VALUE_BIGGER, SKILLS_ERROR_BASE_SKILL, \
    SKILLS_ERROR_DESIRED_SKILL
from the_elder_commands.utils import Skills


class SkillsValidationError(Exception):
    pass


class ValidateSkills:
    def __init__(self, request):
        self.request = request
        self.errors = []
        self.desired_level = self._desired_level_validation()
        self.multiplier = self._priority_multiplier_validation()
        self.fill_skills = self._get_fill_skills()
        self.skills = self.prepare_skills()

    def is_valid(self):
        return self.errors == []

    def _desired_level_validation(self):
        desired_level = self.request.POST.get("desired_level")
        try:
            level = int(desired_level)
            if 81 >= level >= 1:
                return level
            self.errors.append(SKILLS_ERROR_DESIRED_LEVEL_RANGE)
        except ValueError:
            self.errors.append(SKILLS_ERROR_DESIRED_LEVEL)

    def _priority_multiplier_validation(self):
        multiplier = self.request.POST.get("priority_multiplier")
        try:
            return float(multiplier)
        except ValueError:
            self.errors.append(SKILLS_ERROR_MULTIPLIER)

    def prepare_skills(self):
        base_skills = copy.deepcopy(DEFAULT_SKILLS)
        for skills in base_skills.values():
            for skill, properties in skills.items():
                skill_name = properties.get("name")
                default_skill = self._get_default_skill(skill, skill_name)
                desired_skill = self._get_desired_skill(skill, skill_name)
                multiplier = self._get_multiplier(skill)
                if not self.is_new_skill_bigger(default_skill, desired_skill):
                    self.errors.append(SKILLS_ERROR_NEW_VALUE_BIGGER.format(skill=skill_name))
                properties.update({
                  "default_value": default_skill,
                  "desired_value": desired_skill,
                  "multiplier": multiplier
                })
        return base_skills

    @staticmethod
    def is_new_skill_bigger(default_skill, desired_skill):
        try:
            return default_skill <= desired_skill
        except TypeError:
            return True

    def _get_default_skill(self, skill, skill_name):
        try:
            value = int(self.request.POST.get(f"{skill}_base"))
            if 15 <= value <= 100:
                return value
        except ValueError:
            pass
        self.errors.append(SKILLS_ERROR_BASE_SKILL.format(skill=skill_name))

    def _get_desired_skill(self, skill, skill_name):
        value = self.request.POST.get(f"{skill}_new")
        if value == "":
            return value
        try:
            value = int(value)
            if 15 <= value <= 100:
                return value
        except ValueError:
            pass
        self.errors.append(SKILLS_ERROR_DESIRED_SKILL.format(skill=skill_name))

    def _get_multiplier(self, skill):
        multiplier = self.request.POST.get(f"{skill}_multiplier")
        return multiplier == "on"

    def _get_fill_skills(self):
        return self.request.POST.get("fill_skills")

    def save(self):
        if self.is_valid():
            skills = Skills(self.request)
            skills.save_skills(self.skills)
            skills.save_desired_level(self.desired_level)
            skills.save_multiplier(self.multiplier)
            skills.save_fill_skills(self.fill_skills)
        else:
            raise SkillsValidationError(self.errors)