from .models import Character
from .inventory import PLAYABLE_RACES, DEFAULT_SKILLS, RACES_EXTRA_SKILLS
from django.core.exceptions import ObjectDoesNotExist
import copy


class CharacterService:
    def __init__(self, session_key):
        try:
            character = Character.objects.get(session_key=session_key)
        except ObjectDoesNotExist:
            character = Character.objects.create(session_key=session_key)

        self.playable_races = PLAYABLE_RACES
        self.race = character.race
        self.default_skills = self.race_skill_update(character.race)

    @staticmethod
    def race_skill_update(race):
        skills_tree = copy.deepcopy(DEFAULT_SKILLS)
        for category, skills in RACES_EXTRA_SKILLS[race][10].items():
            skills_tree[category][skills]["value"] += 10
        for category, skills in RACES_EXTRA_SKILLS[race][5].items():
            for skill in skills:
                skills_tree[category][skill]["value"] += 5
        return skills_tree

