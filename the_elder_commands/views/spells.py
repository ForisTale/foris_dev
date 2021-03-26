from django.http import JsonResponse
from django.shortcuts import redirect, render

from the_elder_commands.inventory import NO_PLUGIN_SELECTED_ERROR_MESSAGE, COMMANDS_SUCCESS_MESSAGE, \
    SPELLS_COMMANDS_POST_EMPTY_MESSAGE
from the_elder_commands.utils.chosen import ChosenSpells
from the_elder_commands.utils.commands import Commands
from the_elder_commands.utils.convert_value_post import convert_value_post
from the_elder_commands.utils.messages_system import MessagesSystem
from the_elder_commands.utils.selected_plugins import SelectedPlugins


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