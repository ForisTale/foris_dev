from django.shortcuts import render, redirect
from django.http import QueryDict
from .models import Character
from .forms import CharacterForm, PluginsForm
from .services import CharacterService
from .inventory import SKILLS_CONSOLE_NAME
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
    if request.method == "POST":
        data = correct_add_plugin_post(request)
        form = PluginsForm(data=data)
        if form.is_valid():
            form.save()
            return redirect("tec:plugins")
    return render(request, "the_elder_commands/plugins.html", {"active": "plugins"})


def commands_view(request):
    return render(request, "the_elder_commands/commands.html", {"active": "commands"})


def correct_add_plugin_post(request):
    file_content = extract_dict_from_plugin_file(request)
    new_post = request.POST.copy()
    new_post["plugin_data"] = file_content
    new_post._mutable = False
    return new_post


def extract_dict_from_plugin_file(request):
    file = request.FILES["plugin_file"]
    converted_to_dict = json.load(file)
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
    post = {**unpacked_post, "skills": default_race}
    new_post.update(post)
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
