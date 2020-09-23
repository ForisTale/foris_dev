import json
import requests as recaptcha_request
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.shortcuts import reverse
from django.conf import settings
from .inventory import RACES_EXTRA_SKILLS, DEFAULT_SKILLS
from .models import PluginVariants
import copy


class MessagesSystem:
    def __init__(self, request):
        self.request = request
        self._items_key = "items_messages"
        self._plugins_key = "plugins_messages"
        self._skills_key = "skills_messages"
        self._spells_key = "spells_messages"
        self._other_key = "other_messages"
        self._contact_key = "contact_messages"

    def append_plugin(self, message):
        self._append_message(self._plugins_key, message)

    def append_item(self, message):
        self._append_message(self._items_key, message)

    def append_skills(self, message):
        self._append_message(self._skills_key, message)

    def append_spells(self, message):
        self._append_message(self._spells_key, message)

    def append_other(self, message):
        self._append_message(self._other_key, message)

    def append_contact(self, message):
        self._append_message(self._contact_key, message)

    def _append_message(self, key, message):
        if type(message) == list:
            try:
                self._append_message(key, message.pop(0))
                self._append_message(key, message)
            except IndexError:
                pass
        else:
            new_message = self.request.session.get(key, [])
            new_message.append(message)
            self.request.session.update({key: new_message})

    def pop_items(self):
        return self._pop_messages(self._items_key)

    def pop_plugins(self):
        return self._pop_messages(self._plugins_key)

    def pop_skills(self):
        return self._pop_messages(self._skills_key)

    def pop_spells(self):
        return self._pop_messages(self._spells_key)

    def pop_other(self):
        return self._pop_messages(self._other_key)

    def pop_contact(self):
        return self._pop_messages(self._contact_key)

    def _pop_messages(self, key):
        message = self.request.session.get(key, [])
        self.request.session.update({key: []})
        return message


class Commands:
    def __init__(self, request):
        self.request = request
        self._skills_key = "skills_commands"
        self._items_key = "items_commands"
        self._spells_key = "spells_commands"
        self._other_key = "other_commands"

    def set_skills(self, commands):
        self.request.session.update({self._skills_key: commands})

    def set_items(self, items):
        commands = []
        for form_id, quantity in items.items():
            commands.append(f"player.additem {form_id} {quantity}")
        self.request.session.update({self._items_key: commands})

    def set_spells(self, spells):
        commands = []
        for form_id in spells.keys():
            commands.append(f"player.addspell {form_id}")
        self.request.session.update({self._spells_key: commands})

    def set_other(self, various):
        commands = []
        commands += self._prepare_variety_commands(various)
        commands += self._prepare_words_of_power_commands(various)
        commands += self._prepare_perks_commands(various)
        commands += self._prepare_location_commands(various)
        self.request.session.update({self._other_key: commands})

    @staticmethod
    def _prepare_variety_commands(various):
        commands = []
        if various.get("gold"):
            commands.append(f"player.additem 0000000F {various.get('gold')}")
        if various.get("dragon_souls"):
            commands.append(f"player.modav dragonsouls {various.get('dragon_souls')}")
        if various.get("health"):
            commands.append(f"player.modav health {various.get('health')}")
        if various.get("magicka"):
            commands.append(f"player.modav magicka {various.get('magicka')}")
        if various.get("stamina"):
            commands.append(f"player.modav stamina {various.get('stamina')}")
        if various.get("carry_weight"):
            commands.append(f"player.modav carryweight {various.get('carry_weight')}")
        if various.get("movement_speed"):
            commands.append(f"player.setav speedmult {various.get('movement_speed')}")
        return commands

    @staticmethod
    def _prepare_location_commands(various):
        location = various.get("location")
        locations_ids = {
            "Whiterun": "Whiterun",
            "Eldergleam Sanctuary": "EldergleamSanctuaryExterior",
            "Solitude": "Solitude",
            "Windhelm": "Windhelm",
            "Markarth": "MarkarthOrigin",
            "Riften": "RiftenOrigin",
            "Morthal": "MorthalExterior01",
            "Dawnstar": "DawnstarExterior01",
            "Winterhold": "WinterholdExterior01",
            "Falkreath": "FalkreathExterior01",
            "Riverwood": "Riverwood",
            "Dragon Bridge": "DragonBridgeExterior01",
            "Karthwasten": "KarthwastenExterior01",
            "Ivarstead": "IvarsteadExterior01",
            "Helgen": "HelgenExterior",
            "Shor's Stone": "ShorsStoneExterior01",
            "The Atronach Stone": "DoomstoneVolcanicTundra",
            "The Lady Stone": "DoomstonePineForest01",
            "The Lord Stone": "DoomstoneSnowy02",
            "The Lover Stone": "DoomstoneReach01",
            "The Mage Stone": "GuardianStones",
            "The Ritual Stone": "DoomstoneTundra01",
            "The Serpent Stone": "DoomstoneNorthernCoast01",
            "The Shadow Stone": "DoomstoneFallForest01",
            "The Steed Stone": "DoomstoneNorthernPineForest01",
            "The Thief Stone": "GuardianStones",
            "The Tower Stone": "DoomstoneSnowy01",
            "The Warrior Stone": "GuardianStones",
            "The Apprentice Stone": "DoomstoneTundraMarsh01",
            "Rorikstead": "RoriksteadExterior01",
            "Mixwater Mill": "MixwaterMillExterior",
            "Mzulft": "Mzulft01",
            "Sacellum of Boethiah": "DA02BoethiahShrine",
            "Darkwater Crossing": "DarkwaterCrossingExterior01",
            "Kynesgrove": "Kynesgrove",
            "Narzulbur": "Narzulburexterior01",
            "Lakeview Manor": "BYOHHouse1Exterior",
            "Forgotten Vale": "FalmerValleyStart",
            "Mor Khazgur": "MorKhazgurExterior",
            "Stonehills": "StonehillsExterior01",
            "Raven Rock": "DLC2RavenRock01",
            "Skaal Village": "DLC2SkaalVillage01",
            "Soul Cairn": "DLC01SoulCairnOrigin",
            "Sovngarde": "Sovngarde01",
            "Blackreach": "BlackreachCity",
            "Anga's Mill": "AngasMill",
            "Dushnikh Yal": "DushnikhYalExterior01",
            "Largashbur": "LargashburExterior01",
        }
        if location:
            return [f"coc {locations_ids.get(location)}"]
        return []

    @staticmethod
    def _prepare_words_of_power_commands(various):
        words = [word[4:] for word in various.keys() if word[:4] == "word"]
        commands = [f"player.teachword {word}" for word in words]
        return commands

    @staticmethod
    def _prepare_perks_commands(various):
        perks = [perk[4:] for perk in various.keys() if perk[:4] == "perk"]
        commands = [f"player.addperk {perk}" for perk in perks]
        return commands

    def get_commands(self):
        commands = []
        commands += self.request.session.get(self._skills_key, [])
        commands += self.request.session.get(self._items_key, [])
        commands += self.request.session.get(self._spells_key, [])
        commands += self.request.session.get(self._other_key, [])
        return commands


class BaseChosen:
    def __init__(self, request):
        self.request = request
        self._key = None

    def set(self, value):
        self.request.session.update({self._key: value})

    def get(self):
        return self.request.session.get(self._key, {})


class ChosenItems(BaseChosen):
    def __init__(self, *args):
        super().__init__(*args)
        self._key = "chosen_items"


class ChosenSpells(BaseChosen):
    def __init__(self, *args):
        super().__init__(*args)
        self._key = "chosen_spells"


class ChosenOther(BaseChosen):
    def __init__(self, *args):
        super().__init__(*args)
        self._key = "chosen_other"


class SelectedPlugins:
    def __init__(self, request):
        self.request = request
        self._key = "selected"
        self._unselect_key = "unselect"

    def exist(self):
        selected_plugins = self.request.session.get(self._key)
        if selected_plugins:
            for selected in selected_plugins:
                try:
                    PluginVariants.objects.get(instance__name=selected.get("name"), language=selected.get("language"),
                                               version=selected.get("version"), is_esl=selected.get("is_esl"))
                except ObjectDoesNotExist:
                    self.request.session.update({self._key: []})
                    return False
            return True
        return False

    def set(self, selected):
        self.request.session.update({self._key: selected})

    def get(self):
        return self.request.session.get(self._key, [])

    def _unselect_one(self, usable_name):
        all_selected = self.request.session.get(self._key, [])
        for selected in all_selected:
            if selected.get("usable_name") == usable_name:
                all_selected.remove(selected)
        self.request.session.update({self._key: all_selected})

    def _unselect_all(self):
        self.request.session.update({self._key: []})

    def unselect(self):
        post = self.request.POST
        usable_name = post.get(self._unselect_key)
        if usable_name == "unselect_all":
            self._unselect_all()
        else:
            self._unselect_one(usable_name)


def escape_js(string):
    escape = {'&': '\\u0026', '<': '\\u003c', '>': '\\u003e', '\u2028': '\\u2028', '\u2029': '\\u2029'}
    for unsafe, safe in escape.items():
        string = string.replace(unsafe, safe)
    return string


def escape_html(string):
    escape = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '\'': '&#39;', '\"': '&quot;'}
    for unsafe, safe in escape.items():
        string = string.replace(unsafe, safe)
    return string


def default_skills_race_update(race):
    skills_tree = copy.deepcopy(DEFAULT_SKILLS)
    for category, skills in RACES_EXTRA_SKILLS[race][10].items():
        skills_tree[category][skills]["default_value"] += 10
    for category, skills in RACES_EXTRA_SKILLS[race][5].items():
        for skill in skills:
            skills_tree[category][skill]["default_value"] += 5
    return skills_tree


class Skills:
    def __init__(self, request):
        self.request = request
        self._race_key = "race"
        self._default_race = "nord"
        self._skills_key = "skills"
        self._desired_level_key = "desired_level"
        self._multiplier_key = "multiplier"
        self._fill_skills_key = "fill_skills"

    def save_skills(self, skills):
        self.request.session.update({self._skills_key: skills})

    def save_desired_level(self, desired_level):
        self.request.session.update({self._desired_level_key: desired_level})

    def save_multiplier(self, multiplier):
        self.request.session.update({self._multiplier_key: multiplier})

    def save_race(self, race):
        self.request.session.update({self._race_key: race})

    def save_fill_skills(self, value):
        self.request.session.update({self._fill_skills_key: value})

    def get_race(self):
        return self.request.session.get(self._race_key, self._default_race)

    def get_skills(self):
        return self.request.session.get(self._skills_key, default_skills_race_update(self._default_race))

    def get_desired_level(self):
        return self.request.session.get(self._desired_level_key, 1)

    def get_multiplier(self):
        return self.request.session.get(self._multiplier_key, 1.5)

    def get_fill_skills(self):
        return self.request.session.get(self._fill_skills_key)


def convert_value_post(request):
    table_input = request.POST.get("table_input")
    if table_input is None:
        return {}
    parsed_input = json.loads(table_input)
    converted = convert_value_input(parsed_input)
    return converted


def convert_value_input(parsed_input):
    converted = {}
    for item in parsed_input:
        if item.get("value") == "":
            continue
        command = {item.get("name"): item.get("value")}
        converted.update(command)
    return converted


def check_recaptcha(site):
    def decorator(func):
        def wrapper(request):
            recaptcha_data = {"response": request.POST.get("g-recaptcha-response"),
                              "secret": settings.RECAPTCHA_SECRET_KEY}
            recaptcha_response = recaptcha_request.post("https://www.google.com/recaptcha/api/siteverify",
                                                        recaptcha_data)
            result = json.loads(recaptcha_response.content)
            if result.get("success") and result.get("score") >= 0.4:
                func(request)
            else:
                messages = MessagesSystem(request)
                url = HttpRequest.build_absolute_uri(request, reverse('main_page:about_me'))
                getattr(messages, "append_" + site)("It looks like you're a bot. If not, contact me the other way. "
                                                    f"{url}")
        return wrapper
    return decorator
