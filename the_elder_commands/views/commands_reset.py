from django.shortcuts import redirect

from the_elder_commands.utils.chosen import ChosenItems, ChosenSpells, ChosenOther
from the_elder_commands.utils.commands import Commands
from the_elder_commands.utils.defauld_skills_race_update import default_skills_race_update
from the_elder_commands.utils.skills import Skills


def commands_reset_view(request):
    reset_skills(request)
    reset_chosen(request)
    reset_commands(request)
    return redirect("tec:commands")


def reset_skills(request):
    skills = Skills(request)
    race = skills.get_race()
    skills_after_reset = default_skills_race_update(race)
    skills.save_skills(skills_after_reset)
    skills.save_fill_skills(None)


def reset_commands(request):
    commands = Commands(request)
    commands.set_skills([])
    commands.set_items({})
    commands.set_spells({})
    commands.set_other({})


def reset_chosen(request):
    ChosenItems(request).set({})
    ChosenSpells(request).set({})
    ChosenOther(request).set({})