from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from .forms.add_plugins_form import AddPluginsForm
from .forms.selected_plugin_form import SelectedPluginsForm
from .forms.validate_skills import ValidateSkills
from .services import PluginsService, SkillsService
from .inventory import ADD_PLUGIN_SUCCESS_MESSAGE, NO_PLUGIN_SELECTED_ERROR_MESSAGE, COMMANDS_SUCCESS_MESSAGE, \
    ITEMS_COMMANDS_POST_EMPTY_MESSAGE, CONVERT_POST_JS_ERROR, SPELLS_COMMANDS_POST_EMPTY_MESSAGE
from .utils import MessagesSystem, Commands, ChosenItems, SelectedPlugins, Skills, default_skills_race_update, \
    ChosenSpells
import json
from io import BytesIO


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
        items = convert_items_post(request)
        ChosenItems(request).set(items)
        Commands(request).set_items(items)
        if items:
            message = COMMANDS_SUCCESS_MESSAGE
        else:
            message = ITEMS_COMMANDS_POST_EMPTY_MESSAGE
        return JsonResponse({"message": message})

    messages = MessagesSystem(request).pop_items()
    return render(request, "the_elder_commands/items.html", {"active": "items", "messages": messages})


def convert_items_post(request):
    table_input = request.POST.get("table_input")
    if table_input is None:
        MessagesSystem(request).append_item(CONVERT_POST_JS_ERROR)
        return {}
    parsed_input = json.loads(table_input)
    converted = convert_items_input(parsed_input)
    return converted


def convert_items_input(parsed_input):
    converted = {}
    for item in parsed_input:
        if item.get("value") == "":
            continue
        command = {item.get("name"): item.get("value")}
        converted.update(command)
    return converted


def spells_view(request):
    if not SelectedPlugins(request).exist():
        MessagesSystem(request).append_plugin(NO_PLUGIN_SELECTED_ERROR_MESSAGE)
        return redirect("tec:plugins")

    if request.method == "POST":
        spells = convert_spells_post(request)
        ChosenSpells(request).set(spells)
        Commands(request).set_spells(spells)
        if spells:
            message = COMMANDS_SUCCESS_MESSAGE
        else:
            message = SPELLS_COMMANDS_POST_EMPTY_MESSAGE
        return JsonResponse({"message": message})
    message = MessagesSystem(request).pop_spells()
    return render(request, "the_elder_commands/spells.html", {"active": "spells", "messages": message})


def convert_spells_post(request):
    table_input = request.POST.get("table_input")
    if table_input is None:
        MessagesSystem(request).append_spells(CONVERT_POST_JS_ERROR)
        return {}
    parsed_input = json.loads(table_input)
    converted = convert_spells_input(parsed_input)
    return converted


def convert_spells_input(parsed_input):
    converted = {}
    for item in parsed_input:
        if item.get("value") == "":
            continue
        command = {item.get("name"): True}
        converted.update(command)
    return converted


def other_view(request):
    return render(request, "the_elder_commands/other.html", {"active": "other"})


def plugins_view(request):
    if request.method == "POST":
        if "add_plugin" in request.POST:
            manage_add_plugin_post(request)
        elif "selected" in request.POST:
            manage_selected_post(request)
        elif "unselect" in request.POST:
            manage_unselect_post(request)
        return redirect("tec:plugins")

    service = PluginsService(request)
    messages = MessagesSystem(request).pop_plugins()
    return render(request, "the_elder_commands/plugins.html", {"active": "plugins", "service": service,
                                                               "plugins_messages": messages})


def manage_add_plugin_post(request):
    form = AddPluginsForm(request)
    if form.is_valid():
        MessagesSystem(request).append_plugin(ADD_PLUGIN_SUCCESS_MESSAGE)
    else:
        MessagesSystem(request).append_plugin(form.errors)


def manage_selected_post(request):
    form = SelectedPluginsForm(request=request)
    MessagesSystem(request).append_plugin(form.errors)


def manage_unselect_post(request):
    selected = SelectedPlugins(request)
    selected.unselect()


def commands_view(request):
    commands = Commands(request).get_commands()
    return render(request, "the_elder_commands/commands.html", {"active": "commands",
                                                                "commands": commands})


def commands_download(request):
    commands = Commands(request).get_commands()
    content = "\n".join(commands)
    encoded = content.encode("utf-8")
    file = BytesIO(encoded)
    return FileResponse(file, as_attachment=True, filename="TEC_Commands.txt")
