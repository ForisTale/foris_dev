from django.http import JsonResponse
from django.shortcuts import redirect, render

from the_elder_commands.inventory.messages import NO_PLUGIN_SELECTED_ERROR_MESSAGE, COMMANDS_SUCCESS_MESSAGE, \
    ITEMS_COMMANDS_POST_EMPTY_MESSAGE
from the_elder_commands.utils.chosen import ChosenItems
from the_elder_commands.utils.commands import Commands
from the_elder_commands.utils.convert_value_post import convert_value_post
from the_elder_commands.utils.messages_system import MessagesSystem
from the_elder_commands.utils.selected_plugins import SelectedPlugins


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