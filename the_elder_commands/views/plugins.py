import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render

from the_elder_commands.forms.add_plugins_form import AddPluginsForm
from the_elder_commands.forms.selected_plugin_form import SelectedPluginsForm
from the_elder_commands.inventory.messages import ADD_PLUGIN_SUCCESS_MESSAGE, SELECTED_PLUGINS_SUCCESS
from the_elder_commands.services.plugins import PluginsService
from the_elder_commands.utils.check_recaptcha import check_recaptcha
from the_elder_commands.utils.messages_system import MessagesSystem
from the_elder_commands.utils.selected_plugins import SelectedPlugins


def plugins_view(request):
    if request.method == "POST":
        if "add_plugin" in request.POST:
            manage_add_plugin_post(request)
            return redirect("tec:plugins")
        elif "unselect" in request.POST:
            manage_unselect_post(request)
            return redirect("tec:plugins")
        if "selected_plugins" in request.POST:
            manage_selected_post(request)
            return JsonResponse({})

    service = PluginsService(request)
    messages = MessagesSystem(request).pop_plugins()
    zedit_data = get_zedit_data()
    return render(request, "the_elder_commands/plugins.html", {"active": "plugins", "service": service,
                                                               "messages": messages, "zedit": zedit_data,
                                                               "site_key": settings.RECAPTCHA_SITE_KEY})


@check_recaptcha("plugin")
def manage_add_plugin_post(request):
    form = AddPluginsForm(request)
    if form.is_valid():
        MessagesSystem(request).append_plugin(ADD_PLUGIN_SUCCESS_MESSAGE)
    else:
        MessagesSystem(request).append_plugin(form.errors)


def manage_selected_post(request):
    form = SelectedPluginsForm(request)
    if form.is_valid():
        MessagesSystem(request).append_plugin(SELECTED_PLUGINS_SUCCESS)
    else:
        MessagesSystem(request).append_plugin(form.errors)


def manage_unselect_post(request):
    selected = SelectedPlugins(request)
    selected.unselect()


def get_zedit_data():
    path = os.getcwd()
    path = os.path.join(path, "the_elder_commands", "script_for_zEdit.js")
    with open(path, "r") as file:
        return file.read()