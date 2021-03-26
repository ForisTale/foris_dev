from io import BytesIO

from django.http import FileResponse

from the_elder_commands.utils.commands import Commands


def commands_download_view(request):
    commands = Commands(request).get_commands()
    content = "\n".join(commands)
    encoded = content.encode("utf-8")
    file = BytesIO(encoded)
    return FileResponse(file, as_attachment=True, filename="TEC_Commands.txt")