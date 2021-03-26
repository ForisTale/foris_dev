from django.shortcuts import render

from the_elder_commands.utils.commands import Commands


def commands_view(request):
    commands = Commands(request).get_commands()
    return render(request, "the_elder_commands/commands.html", {"active": "commands",
                                                                "commands": commands})