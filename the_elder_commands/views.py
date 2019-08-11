from django.shortcuts import render, redirect
from .models import Character
from .forms import CharacterForm
from .services import CharacterService
from .inventory import SKILLS_CONSOLE_NAME


def character_view(request):
    if not request.session.session_key:
        request.session.save()

    if request.method == "POST":
        instance = Character.objects.get_or_create(session_key=request.session.session_key)[0]

        unpacked_post = unpack_post(request.POST)
        default, desired = extract_skills(unpacked_post)

        if "race" in request.POST:
            default_skills = CharacterService.default_race_skills_update(unpacked_post["race"])
            set_skills_values(default, default_skills)
            post = {
                **unpacked_post,
                "default_skills": default_skills,
            }
        else:
            default_skills = CharacterService.default_race_skills_update(instance.race)
            desired_skills = CharacterService.default_race_skills_update(instance.race)
            set_skills_values(default, default_skills)
            set_skills_values(desired, desired_skills)
            post = {
                **unpacked_post,
                "default_skills": default_skills,
                "desired_skills": desired_skills,
            }
        form = CharacterForm(data=post, instance=instance)
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
            value = post.pop(key)
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
                skill_value = skills_value[skill["console_name"]]
                if skill_value == "":
                    value = ""
                else:
                    value = int(skill_value)
                skill["value"] = value
