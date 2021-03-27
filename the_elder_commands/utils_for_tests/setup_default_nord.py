import copy

from the_elder_commands.inventory.defaults_for_skills import DEFAULT_SKILLS


def setup_default_nord():
    skills = copy.deepcopy(DEFAULT_SKILLS)
    skills["Combat"]["twohanded"]["default_value"] += 10
    skills["Stealth"]["speechcraft"]["default_value"] += 5
    skills["Stealth"]["lightarmor"]["default_value"] += 5
    for skill in ["block", "onehanded", "smithing"]:
        skills["Combat"][skill]["default_value"] += 5
    return skills