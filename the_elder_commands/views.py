from django.shortcuts import render, redirect
from django.http import QueryDict
from .models import Character
from .forms import CharacterForm, PluginsForm, PluginVariantsForm
from .services import CharacterService, PluginsService
from .inventory import SKILLS_CONSOLE_NAME, ADD_PLUGIN_SUCCESS_MESSAGE
import json


def character_view(request):
    if not request.session.session_key:
        request.session.save()
    form = None
    if request.method == "POST":
        instance = Character.objects.get_or_create(session_key=request.session.session_key)[0]
        if "race" in request.POST:
            skills = CharacterService.default_race_skills_update(request.POST["race"])
            post = {**unpack_post(request.POST), "skills": skills}
        else:
            post = correct_character_post(request.POST, instance.race)
        form = CharacterForm(data=post, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(instance)
    character = CharacterService(session_key=request.session.session_key)
    return render(request, "the_elder_commands/character.html", {"character": character, "form": form,
                                                                 "active": "character"})


def items_view(request):
    return render(request, "the_elder_commands/items.html", {"active": "items"})


def spells_view(request):
    return render(request, "the_elder_commands/spells.html", {"active": "spells"})


def other_view(request):
    return render(request, "the_elder_commands/other.html", {"active": "other"})


def plugins_view(request):
    if "add_plugin_messages" in request.session:
        add_plugin_messages, request.session["add_plugin_messages"] = request.session["add_plugin_messages"], []
    else:
        request.session["add_plugin_messages"] = []
        add_plugin_messages = []

    if request.method == "POST":
        plugin_custom_form = PluginsForm(name=request.POST.get("plugin_name", ""))

        if plugin_custom_form.is_valid():

            plugin_variants_data = plugin_variants_post(request)
            plugin_variants_form = PluginVariantsForm(data=plugin_variants_data,
                                                      instance=plugin_custom_form.instance)

            if plugin_variants_form.is_valid():

                plugin_variants_form.save()
                request.session["add_plugin_messages"].append(ADD_PLUGIN_SUCCESS_MESSAGE)
                return redirect("tec:plugins")
            else:
                for error in plugin_variants_form.errors.values():
                    add_plugin_messages = [*add_plugin_messages, *error]
        else:
            for error in plugin_custom_form.errors:
                add_plugin_messages = [*add_plugin_messages, *error]

    plugins = PluginsService(request)
    return render(request, "the_elder_commands/plugins.html", {"active": "plugins", "plugins": plugins.all_plugins,
                                                               "add_plugin_messages": add_plugin_messages})


def commands_view(request):
    return render(request, "the_elder_commands/commands.html", {"active": "commands"})


def plugin_variants_post(request):
    file_content = extract_dict_from_plugin_file(request)
    post = QueryDict("", mutable=True)
    post["version"] = request.POST.get("plugin_version")
    post["language"] = request.POST.get("plugin_language")
    post["plugin_data"] = file_content
    return post


def extract_dict_from_plugin_file(request):
    file = request.FILES["plugin_file"]
    try:
        converted_to_dict = json.load(file)
    except json.decoder.JSONDecodeError as e:
        print("JSON error in view: ", e.msg)
        return {}
    return converted_to_dict


def unpack_post(post):
    corrected = {}
    for key, value in post.items():
        if len(value) == 1:
            corrected[key] = value[0]
        else:
            corrected[key] = value
    return corrected


def correct_character_post(post, race):
    unpacked_post = unpack_post(post)
    skills = extract_skills(unpacked_post)
    default_race = CharacterService.default_race_skills_update(race)
    set_skills_values(skills, default_race)

    new_post = QueryDict("", mutable=True)
    new_post.update({**unpacked_post, "skills": default_race})
    new_post._mutable = False
    return new_post


def extract_skills(post):
    skills = {"default": {}, "desired": {}, "multiplier": {}}
    keys = []
    keys += post.keys()
    for key in keys:
        spacer_index = key.find("_")
        skill = key[:spacer_index]
        if skill in SKILLS_CONSOLE_NAME:
            value = post.pop(key)
            ending = key[spacer_index:]
            if ending == "_base":
                skills["default"][skill] = value
            elif ending == "_new":
                skills["desired"][skill] = value
            elif ending == "_multiplier":
                skills["multiplier"][skill] = True
    return skills


def set_skills_values(skills_value, dictionary):
    for skills in dictionary.values():
        for skill in skills.values():
            for kind in skills_value.keys():
                if skill["console_name"] in skills_value[kind].keys():
                    skill_value = skills_value[kind][skill["console_name"]]
                    if skill_value is True:
                        skill["multiplier"] = True
                        continue
                    if skill_value == "":
                        value = ""
                    else:
                        value = skill_value
                    skill[kind + "_value"] = value
