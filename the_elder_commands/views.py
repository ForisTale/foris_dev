from django.shortcuts import render, redirect
from django.http import QueryDict, JsonResponse, FileResponse
from .forms import PluginsForm, PluginVariantsForm, SelectedPluginsForm, ValidateSkills
from .services import PluginsService, SkillsService
from .inventory import ADD_PLUGIN_SUCCESS_MESSAGE, NO_PLUGIN_SELECTED_ERROR_MESSAGE, COMMANDS_SUCCESS_MESSAGE, \
    ITEMS_COMMANDS_POST_EMPTY_MESSAGE, ITEMS_CONVERT_POST_ERROR, ADD_PLUGIN_FILE_ERROR_MESSAGE, \
    ADD_PLUGIN_PLUGIN_EXIST_ERROR_MESSAGE
from .utils import MessagesSystem, Commands, ChosenItems, SelectedPlugins, Skills, default_race_skills_update
import json
from io import BytesIO


def skills_view(request):
    message_system = MessagesSystem(request)
    if request.method == "POST":
        if "race" in request.POST:
            race = request.POST.get("race")
            reset_skills = default_race_skills_update(race)
            skills = Skills(request)
            skills.save_race(race)
            skills.save_skills(reset_skills)
            skills.save_fill_skills(None)
        else:
            form = ValidateSkills(request)
            if form.is_valid():
                form.save()
                message_system.append_skills(COMMANDS_SUCCESS_MESSAGE)
            else:
                message_system.append_skills(form.errors)
        return redirect("tec:skills")

    message = message_system.pop_skills()
    service = SkillsService(request)
    Commands(request).set_skills(service.commands)
    return render(request, "the_elder_commands/skills.html", {"service": service, "messages": message,
                                                              "active": "skills"})


def items_view(request):
    message_system = MessagesSystem(request)

    if not SelectedPlugins(request).exist():
        message_system.append_plugin(NO_PLUGIN_SELECTED_ERROR_MESSAGE)
        return redirect("tec:plugins")

    if request.method == "POST":
        commands = convert_items_post(request)
        ChosenItems(request).set(commands)
        Commands(request).set_items(commands)
        if commands:
            message = COMMANDS_SUCCESS_MESSAGE
        else:
            message = ITEMS_COMMANDS_POST_EMPTY_MESSAGE
        return JsonResponse({"message": message})

    messages = message_system.pop_items()
    return render(request, "the_elder_commands/items.html", {"active": "items", "items_messages": messages})


def spells_view(request):
    return render(request, "the_elder_commands/spells.html", {"active": "spells"})


def other_view(request):
    return render(request, "the_elder_commands/other.html", {"active": "other"})


def plugins_view(request):
    messages_system = MessagesSystem(request)

    if request.method == "POST":
        if "add_plugin" in request.POST:
            handle_add_plugin_post(request)
            return redirect("tec:plugins")
        elif "selected" in request.POST:
            form = SelectedPluginsForm(request=request)
            messages_system.append_plugin(form.errors)
            return redirect("tec:plugins")
        elif "unselect" in request.POST:
            selected = SelectedPlugins(request)
            selected.unselect(request.POST)
            return redirect("tec:plugins")

    service = PluginsService(request)
    messages = messages_system.pop_plugins()
    return render(request, "the_elder_commands/plugins.html", {"active": "plugins", "service": service,
                                                               "plugins_messages": messages})


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


def handle_add_plugin_post(request):
    messages_system = MessagesSystem(request)
    plugin_custom_form = PluginsForm(name=request.POST.get("plugin_name", ""))
    if plugin_custom_form.is_valid():
        plugin_variants_data = create_variants_data_post(request)
        if plugin_variants_data:
            plugin_variants_form = PluginVariantsForm(data=plugin_variants_data,
                                                      instance=plugin_custom_form.instance)
            if plugin_variants_form.is_valid():
                plugin_variants_form.save()
                messages_system.append_plugin(ADD_PLUGIN_SUCCESS_MESSAGE)
                return
            else:
                for header, error in plugin_variants_form.errors.items():
                    if header == "__all__":
                        messages_system.append_plugin(ADD_PLUGIN_PLUGIN_EXIST_ERROR_MESSAGE)
                        return
                    messages_system.append_plugin([*error])
                return
        else:
            messages_system.append_plugin(ADD_PLUGIN_FILE_ERROR_MESSAGE)
            return
    else:
        for error in plugin_custom_form.errors:
            messages_system.append_plugin(error)
            return


def create_variants_data_post(request):
    file_content = extract_dict_from_plugin_file(request)
    try:
        is_esl = file_content.pop("isEsl")
    except (KeyError, AttributeError):
        return
    post = QueryDict("", mutable=True)
    post.update({"version": request.POST.get("plugin_version"), "language": request.POST.get("plugin_language"),
                 "plugin_data": file_content, "is_esl": is_esl})
    return post


def extract_dict_from_plugin_file(request):
    file = request.FILES.get("plugin_file")
    try:
        return json.load(file)
    except (json.decoder.JSONDecodeError, AttributeError, UnicodeDecodeError):
        pass


def convert_items_post(request):
    messages_system = MessagesSystem(request)
    table_input = request.POST.get("table_input")
    if table_input is None:
        messages_system.append_item(ITEMS_CONVERT_POST_ERROR)
        return {}
    parsed_input = json.loads(table_input)

    converted = {}
    for item in parsed_input:
        if item.get("value") == "":
            continue
        command = {item.get("name"): item.get("value")}
        converted.update(command)
    return converted
