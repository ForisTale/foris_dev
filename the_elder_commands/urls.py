from django.urls import path
from .views import skills_view, items_view, spells_view, other_view, plugins_view, commands_view, commands_download, \
    commands_reset


app_name = "tec"

urlpatterns = [
    path("", skills_view, name="home"),
    path("skills/", skills_view, name="skills"),
    path("items/", items_view, name="items"),
    path("spells/", spells_view, name="spells"),
    path("other/", other_view, name="other"),
    path("plugins/", plugins_view, name="plugins"),
    path("commands/", commands_view, name="commands"),
    path("commands/download", commands_download, name="commands_download"),
    path("commands/reset", commands_reset, name="commands_reset"),
]
