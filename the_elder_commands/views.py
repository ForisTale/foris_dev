from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from django.conf import settings
from .forms.add_plugins_form import AddPluginsForm
from .forms.selected_plugin_form import SelectedPluginsForm
from .forms.validate_skills import ValidateSkills
from .services import PluginsService, SkillsService
from .inventory import ADD_PLUGIN_SUCCESS_MESSAGE, NO_PLUGIN_SELECTED_ERROR_MESSAGE, COMMANDS_SUCCESS_MESSAGE, \
    ITEMS_COMMANDS_POST_EMPTY_MESSAGE, SPELLS_COMMANDS_POST_EMPTY_MESSAGE, OTHER_COMMANDS_POST_EMTPY_MESSAGE, \
    SELECTED_PLUGINS_SUCCESS
from .utils.commands import Commands
from .utils.chosen import ChosenItems,  ChosenSpells, ChosenOther
from .utils.selected_plugins import SelectedPlugins
from .utils.skills import Skills
from .utils.defauld_skills_race_update import default_skills_race_update
from .utils.convert_value_post import convert_value_post
from .utils.check_recaptcha import check_recaptcha
from .utils.messages_system import MessagesSystem
from io import BytesIO
import os


def home_view(request):
    return render(request, "the_elder_commands/home.html")


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


def items_view(request):
    if not SelectedPlugins(request).exist():
        MessagesSystem(request).append_plugin(NO_PLUGIN_SELECTED_ERROR_MESSAGE)
        return redirect("tec:plugins")

    if request.method == "POST":
        items = convert_value_post(request)
        ChosenItems(request).set(items)
        Commands(request).set_items(items)
        if items:
            message = COMMANDS_SUCCESS_MESSAGE
        else:
            message = ITEMS_COMMANDS_POST_EMPTY_MESSAGE
        return JsonResponse({"message": message})

    messages = MessagesSystem(request).pop_items()
    return render(request, "the_elder_commands/items.html", {"active": "items", "messages": messages})


def spells_view(request):
    if not SelectedPlugins(request).exist():
        MessagesSystem(request).append_plugin(NO_PLUGIN_SELECTED_ERROR_MESSAGE)
        return redirect("tec:plugins")

    if request.method == "POST":
        spells = convert_value_post(request)
        ChosenSpells(request).set(spells)
        Commands(request).set_spells(spells)
        if spells:
            message = COMMANDS_SUCCESS_MESSAGE
        else:
            message = SPELLS_COMMANDS_POST_EMPTY_MESSAGE
        return JsonResponse({"message": message})

    message = MessagesSystem(request).pop_spells()
    return render(request, "the_elder_commands/spells.html", {"active": "spells", "messages": message})


def other_view(request):
    if not SelectedPlugins(request).exist():
        MessagesSystem(request).append_plugin(NO_PLUGIN_SELECTED_ERROR_MESSAGE)
        return redirect("tec:plugins")

    if request.method == "POST":
        variety = convert_value_post(request)
        ChosenOther(request).set(variety)
        Commands(request).set_other(variety)
        if variety:
            message = COMMANDS_SUCCESS_MESSAGE
        else:
            message = OTHER_COMMANDS_POST_EMTPY_MESSAGE
        return JsonResponse({"message": message})

    messages = MessagesSystem(request).pop_other()
    chosen = ChosenOther(request).get()
    return render(request, "the_elder_commands/other.html", {"active": "other", "chosen": chosen,
                                                             "messages": messages})


def plugins_view(request):
    if request.method == "POST":
        if "add_plugin" in request.POST:
            manage_add_plugin_post(request)
            return redirect("tec:plugins")
        elif "unselect" in request.POST:
            manage_unselect_post(request)
            return redirect("tec:plugins")
        if "selected_plugins" in request.POST:
            manage_selected_post(request)
            return JsonResponse({})

    service = PluginsService(request)
    messages = MessagesSystem(request).pop_plugins()
    zedit_data = get_zedit_data()
    return render(request, "the_elder_commands/plugins.html", {"active": "plugins", "service": service,
                                                               "messages": messages, "zedit": zedit_data,
                                                               "site_key": settings.RECAPTCHA_SITE_KEY})


@check_recaptcha("plugin")
def manage_add_plugin_post(request):
    form = AddPluginsForm(request)
    if form.is_valid():
        MessagesSystem(request).append_plugin(ADD_PLUGIN_SUCCESS_MESSAGE)
    else:
        MessagesSystem(request).append_plugin(form.errors)


def manage_selected_post(request):
    form = SelectedPluginsForm(request)
    if form.is_valid():
        MessagesSystem(request).append_plugin(SELECTED_PLUGINS_SUCCESS)
    else:
        MessagesSystem(request).append_plugin(form.errors)


def manage_unselect_post(request):
    selected = SelectedPlugins(request)
    selected.unselect()


def get_zedit_data():
    path = os.getcwd()
    path = os.path.join(path, "the_elder_commands", "script_for_zEdit.js")
    with open(path, "r") as file:
        return file.read()


def commands_view(request):
    commands = Commands(request).get_commands()
    return render(request, "the_elder_commands/commands.html", {"active": "commands",
                                                                "commands": commands})


def commands_download_view(request):
    commands = Commands(request).get_commands()
    content = "\n".join(commands)
    encoded = content.encode("utf-8")
    file = BytesIO(encoded)
    return FileResponse(file, as_attachment=True, filename="TEC_Commands.txt")


def commands_reset_view(request):
    reset_skills(request)
    reset_commands(request)
    reset_chosen(request)
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
