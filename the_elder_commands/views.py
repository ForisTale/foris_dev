from django.shortcuts import render
from .forms import CharacterForm


def character_view(request):
    return render(request, "the_elder_commands/character.html", {"character_form": CharacterForm("Nord")})
