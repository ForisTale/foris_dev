from django.http import JsonResponse
from django.shortcuts import redirect, render

from the_elder_commands.inventory import NO_PLUGIN_SELECTED_ERROR_MESSAGE, COMMANDS_SUCCESS_MESSAGE, \
    OTHER_COMMANDS_POST_EMTPY_MESSAGE
from the_elder_commands.utils.chosen import ChosenOther
from the_elder_commands.utils.commands import Commands
from the_elder_commands.utils.convert_value_post import convert_value_post
from the_elder_commands.utils.messages_system import MessagesSystem
from the_elder_commands.utils.selected_plugins import SelectedPlugins


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