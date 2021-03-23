import copy

from the_elder_commands.inventory import DEFAULT_SKILLS, RACES_EXTRA_SKILLS


def default_skills_race_update(race):
    skills_tree = copy.deepcopy(DEFAULT_SKILLS)
    for category, skills in RACES_EXTRA_SKILLS[race][10].items():
        skills_tree[category][skills]["default_value"] += 10
    for category, skills in RACES_EXTRA_SKILLS[race][5].items():
        for skill in skills:
            skills_tree[category][skill]["default_value"] += 5
    return skills_tree