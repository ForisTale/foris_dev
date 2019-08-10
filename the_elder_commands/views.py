from django.shortcuts import render, redirect
from .forms import CharacterForm
from .services import CharacterService
from .inventory import SKILLS_CONSOLE_NAME, DEFAULT_SKILLS
import copy


def character_view(request):
    if not request.session.session_key:
        request.session.save()

    if request.method == "POST":
        unpacked_post = unpack_post(request.POST)

        default, desired = extract_skills(unpacked_post)

        default_skills = copy.deepcopy(DEFAULT_SKILLS)
        desired_skills = copy.deepcopy(DEFAULT_SKILLS)
        set_skills_values(default, default_skills)
        set_skills_values(desired, desired_skills)

        post = {
            **unpacked_post,
            "default_skills": default_skills,
            "desired_skills": desired_skills,
            "session_key": request.session.session_key,
        }
        form = CharacterForm(data=post)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        return redirect("/the_elder_commands/")

    character = CharacterService(session_key=request.session.session_key)
    return render(request, "the_elder_commands/character.html", {"character": character})


def unpack_post(post):
    corrected = {}
    for key, value in post.items():
        if len(value) == 1:
            corrected[key] = value[0]
        else:
            corrected[key] = value
    return corrected


def extract_skills(post):
    default = {}
    desired = {}
    keys = []
    keys += post.keys()
    for key in keys:
        spacer_index = key.find("_")
        skill = key[:spacer_index]
        if skill in SKILLS_CONSOLE_NAME:
            value = int(post.pop(key))
            ending = key[spacer_index:]
            if ending == "_base":
                default[skill] = value
            elif ending == "_new":
                desired[skill] = value

    return default, desired


def set_skills_values(skills_value, dictionary):

    for skills in dictionary.values():
        for skill in skills.values():
            if skill["console_name"] in skills_value.keys():
                value = int(skills_value[skill["console_name"]])
                skill["value"] = value
