from .models import PluginVariants, Plugins
from .utils import ChosenItems, SelectedPlugins, Skills as NewSkills, default_skills_race_update
import math


class SkillsService:
    def __init__(self, request):
        skills = NewSkills(request)
        self.race = skills.get_race()
        self.skills = skills.get_skills()
        self.multiplier = skills.get_multiplier()
        self.fill_skills = skills.get_fill_skills()
        self.default_level = self.predict_level("default")
        self.desired_level = self.predict_desired_level(request)
        self.commands = self.commands_list()

    def predict_level(self, kind):
        default = default_skills_race_update(self.race)
        total_exp = 0
        for category, skills in self.skills.items():
            for name, skill in skills.items():
                default_value = default[category][name]["default_value"]
                if skill.get("desired_value") == "" and kind == "desired":
                    for char_xp in range(default_value + 1, skill.get("default_value") + 1):
                        total_exp += char_xp
                    continue
                if skill[kind + "_value"] > default_value:
                    for char_xp in range(default_value + 1, skill[kind + "_value"] + 1):
                        total_exp += char_xp
        level = (-2.5 + math.sqrt(8 * total_exp + 1225) / 10)
        return int(level)

    def predict_desired_level(self, request):
        skill = NewSkills(request)
        target_level = skill.get_desired_level()
        if self.default_level < target_level and self.fill_skills:
            self.set_skills_to_desired_level(target_level)
            return target_level
        else:
            return self.predict_level("desired")

    def set_skills_to_desired_level(self, target_level):
        total_exp = self.count_needed_exp(target_level)
        values = {}
        while total_exp > 0:
            all_skills_filled = 0
            for category, skills in self.skills.items():
                for skill_name, skill in skills.items():
                    value = values.get(skill_name, 1)
                    while value >= 1:
                        if skill.get("desired_value") == 100:
                            all_skills_filled += 1
                            break
                        if skill.get("desired_value") == "":
                            skill.update({"desired_value": skill.get("default_value") + 1})
                        else:
                            skill.update({"desired_value": skill.get("desired_value") + 1})
                        total_exp -= skill.get("desired_value")
                        value -= 1
                    if skill.get("multiplier"):
                        value += self.multiplier
                    else:
                        value += 1
                    values.update({skill_name: value})
            if all_skills_filled == 18:
                break

    def count_needed_exp(self, target_level):
        predicted_level = self.predict_level("desired")
        predicted_exp = 12.5 * (predicted_level ** 2) + 62.5 * predicted_level - 75
        target_exp = 12.5 * (target_level ** 2) + 62.5 * target_level - 75
        total_exp = target_exp - predicted_exp
        return total_exp

    def commands_list(self):
        total_exp = 0
        commands = []
        for skills in self.skills.values():
            for name, skill in skills.items():
                if skill["desired_value"] == "":
                    continue
                default_value = skill.get("default_value")
                if skill["desired_value"] > default_value:
                    for skill_level in range(default_value, skill.get("desired_value")):
                        skill_xp = skill.get("sim") * (skill_level ** 1.95) + skill.get("sio")
                        total_exp += skill_xp
                    skill_command_value = total_exp / skill.get("sum")
                    total_exp = 0
                    commands.append(f"player.advskill {skill['console_name']} {int(skill_command_value) + 1}")
        return commands


class PluginsService:
    def __init__(self, request):
        self.selected = request.session.get("selected", [])
        self.all_plugins = self.get_all_plugins()

    class Plugin:
        def __init__(self, name, usable_name, selected, load_order, variants):
            self.name = name
            self.usable_name = usable_name
            self.selected = selected
            self.load_order = load_order
            self.variants = variants

    class Variant:
        def __init__(self, language, version, selected, esl):
            self.language = language
            self.version = version
            self.selected = selected
            self.esl = esl

    def get_all_plugins(self):
        plugins = []
        for plugin in Plugins.objects.all():
            variants = self.get_variants(plugin.name)
            if variants:
                plugins.append(self.Plugin(
                    name=plugin.name,
                    usable_name=plugin.usable_name,
                    selected=self.is_plugin_selected(plugin.name),
                    load_order=self.get_load_order(plugin.name),
                    variants=variants
                ))
        return plugins

    def is_plugin_selected(self, plugin_name):
        for selected in self.selected:
            if selected.get("name") == plugin_name:
                return True
        return False

    def get_load_order(self, plugin_name):
        for selected in self.selected:
            if selected.get("name") == plugin_name:
                return selected.get("load_order")
        return ""

    def get_variants(self, plugin_name):
        variants = []
        for variant in PluginVariants.objects.filter(instance__name=plugin_name).order_by("-version", "language"):
            variants.append(self.Variant(language=variant.language, version=variant.version,
                                         selected=self.is_variant_selected(variant), esl=self.get_esl(variant)))
        return variants

    def is_variant_selected(self, variant_instance):
        for selected in self.selected:
            if selected.get("version") == variant_instance.version and \
                    selected.get("language") == variant_instance.language and \
                    variant_instance.instance.name == selected.get("name"):
                return True
        return False

    @staticmethod
    def get_esl(variant):
        return "esl" if variant.is_esl else ""


class ItemsService:
    def __init__(self, request, category):
        self.chosen = ChosenItems(request).get()
        self.selected = SelectedPlugins(request).get()
        self.items = self.get_items(category)

    def get_items(self, category):
        items = []
        for selected in self.selected:
            variant = PluginVariants.objects.get(instance__name=selected.get("name"), version=selected.get("version"),
                                                 language=selected.get("language"))
            variant_items = variant.plugin_data.get(category)
            for item in variant_items:
                form_id = f"{selected.get('load_order')}{item.get('formId')}"
                quantity = self.chosen.get(form_id, "")
                item.update({"formId": form_id, "plugin_name": selected.get("name"), "quantity": quantity,
                             "selected": quantity != ""})
                items.append(item)

        return items
