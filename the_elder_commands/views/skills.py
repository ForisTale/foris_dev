from django.shortcuts import redirect, render

from the_elder_commands.forms.validate_skills import ValidateSkills
from the_elder_commands.inventory.messages import COMMANDS_SUCCESS_MESSAGE
from the_elder_commands.services.skills import SkillsService
from the_elder_commands.utils.commands import Commands
from the_elder_commands.utils.defauld_skills_race_update import default_skills_race_update
from the_elder_commands.utils.messages_system import MessagesSystem
from the_elder_commands.utils.skills import Skills


def skills_view(request):
    if request.method == "POST":
        if "race" in request.POST:
            manage_race_post(request)
        else:
            manage_skills_post(request)
        return redirect("tec:skills")

    message = MessagesSystem(request).pop_skills()
    service = SkillsService(request)
    Commands(request).set_skills(service.commands)
    return render(request, "the_elder_commands/skills.html", {"service": service, "messages": message,
                                                              "active": "skills"})


def manage_race_post(request):
    race = request.POST.get("race")
    reset_skills = default_skills_race_update(race)
    skills = Skills(request)
    skills.save_race(race)
    skills.save_skills(reset_skills)
    skills.save_fill_skills(None)


def manage_skills_post(request):
    form = ValidateSkills(request)
    if form.is_valid():
        form.save()
        MessagesSystem(request).append_skills(COMMANDS_SUCCESS_MESSAGE)
    else:
        MessagesSystem(request).append_skills(form.errors)