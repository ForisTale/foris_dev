from django.urls import path
from .views.home import home_view
from .views.skills import skills_view
from .views.items import items_view
from .views.spells import spells_view
from .views.other import other_view
from .views.plugins import plugins_view
from .views.commands import commands_view
from .views.commands_download import commands_download_view
from .views.commands_reset import commands_reset_view

app_name = "tec"

urlpatterns = [
    path("", home_view, name="home"),
    path("skills/", skills_view, name="skills"),
    path("items/", items_view, name="items"),
    path("spells/", spells_view, name="spells"),
    path("other/", other_view, name="other"),
    path("plugins/", plugins_view, name="plugins"),
    path("commands/", commands_view, name="commands"),
    path("commands/download", commands_download_view, name="commands_download"),
    path("commands/reset", commands_reset_view, name="commands_reset"),
]
