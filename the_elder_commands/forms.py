from django.forms.models import ModelForm
from django.forms import ValidationError
from django.http import QueryDict
from the_elder_commands.models import Plugins, PluginVariants
from the_elder_commands.inventory import ADD_PLUGIN_ERROR_FILE, INCORRECT_LOAD_ORDER, \
    PLUGINS_ERROR_NAME_IS_EMTPY, PLUGINS_ERROR_NAME_BECOME_EMPTY, \
    SKILLS_ERROR_NEW_VALUE_BIGGER, SKILLS_ERROR_DESIRED_LEVEL_RANGE, \
    SKILLS_ERROR_DESIRED_LEVEL, SKILLS_ERROR_MULTIPLIER, DEFAULT_SKILLS, SKILLS_ERROR_DESIRED_SKILL, \
    SKILLS_ERROR_BASE_SKILL, ADD_PLUGIN_ERROR_PLUGIN_EXIST
from the_elder_commands.utils import SelectedPlugins, escape_html, Skills as NewSkills
import copy
import json


class AddPluginsForm:
    def __init__(self, request):
        self.request = request
        self.name = request.POST.get("plugin_name", "")
        self.errors = []

        self.clean_name()
        if self.is_valid():
            self.name = self.cut_special_letters_from_name()
            self.usable_name = self.get_usable_name()
            self.instance, created = Plugins.objects.get_or_create(name=self.name,
                                                                   usable_name=self.usable_name)
            self.handle_variants_form()

    def clean_name(self):
        if self.name == "":
            self.errors.append(PLUGINS_ERROR_NAME_IS_EMTPY)
        elif self.name_become_empty():
            self.errors.append(PLUGINS_ERROR_NAME_BECOME_EMPTY)

    def is_valid(self):
        return self.errors == []

    def name_become_empty(self):
        name = self.cut_special_letters_from_name()
        name = name.strip()
        if name == "":
            return True

    def cut_special_letters_from_name(self):
        converted = ""
        for letter in self.name:
            if letter.isalnum() or letter == " ":
                converted += letter
        return converted

    def get_usable_name(self):
        converted = ""
        for letter in self.name:
            if letter == " ":
                converted += "_"
            else:
                converted += letter.lower()
        return converted

    def handle_variants_form(self):
        if self.is_valid():
            correct_post = self.create_variants_post()
            if correct_post:
                form = PluginVariantsForm(data=correct_post)
                if form.is_valid():
                    form.save()
                else:
                    for header, error in form.errors.items():
                        if header == "__all__":
                            self.errors.append(ADD_PLUGIN_ERROR_PLUGIN_EXIST)
                        else:
                            self.errors.append([*error])
            else:
                self.errors.append(ADD_PLUGIN_ERROR_FILE)

    def create_variants_post(self):
        file_content = self.extract_dict_from_plugin_file()
        is_esl = self.pop_is_esl(file_content)
        if is_esl is not None:
            post = QueryDict("", mutable=True)
            post.update({"version": self.request.POST.get("plugin_version"), "is_esl": is_esl,
                         "language": self.request.POST.get("plugin_language"),
                         "plugin_data": file_content, "instance": self.instance})
            return post

    def extract_dict_from_plugin_file(self):
        file = self.request.FILES.get("plugin_file")
        try:
            return json.load(file)
        except (json.decoder.JSONDecodeError, AttributeError, UnicodeDecodeError):
            pass

    @staticmethod
    def pop_is_esl(file_content):
        try:
            is_esl = file_content.pop("isEsl")
        except (KeyError, AttributeError):
            return
        return is_esl


class PluginVariantsForm(ModelForm):

    class Meta:
        model = PluginVariants
        fields = ("version", "language", "plugin_data", "instance", "is_esl")

        error_messages = {
            "plugin_data": {"required": ADD_PLUGIN_ERROR_FILE},
        }

    def clean_version(self):
        form_data = self.cleaned_data["version"]
        new_version = ""
        for letter in form_data:
            if letter.isalnum():
                new_version += letter
            elif letter in "_-;:,.":
                new_version += letter

        return new_version

    def clean_plugin_data(self):
        plugin_keys = ["WEAP", "ARMO", "BOOK", "INGR", "ALCH", "MISC", "PERK",
                       "AMMO", "SCRL", "SLGM", "KEYM", "SPEL", "WOOP"]
        form_data = self.cleaned_data["plugin_data"]
        new_form_data = {}

        for key in plugin_keys:
            data_value = form_data.get(key)
            if data_value is None:
                raise ValidationError(ADD_PLUGIN_ERROR_FILE)

            new_items = self.escape_items(data_value)
            new_form_data.update({key: new_items})

        return new_form_data

    @staticmethod
    def escape_items(items):
        new_items = []
        try:
            for item in items:
                new_dict = {}
                for key, value in item.items():
                    new_dict.update({key: escape_html(str(value))})
                new_items.append(new_dict)
        except (TypeError, AttributeError):
            raise ValidationError(ADD_PLUGIN_ERROR_FILE)
        return new_items


class SelectedPluginsForm:
    def __init__(self, request):
        self.data = request.POST.copy()
        self.request = request
        self.errors = []

        self.clean_load_order()
        if self.is_valid():
            self.collect_selected()

    def clean_load_order(self):
        selected = self.data.getlist("selected", [])
        for usable_name in selected:
            if usable_name == "":
                continue

            load_order = self.data.get(f"{usable_name}_load_order", "")
            length = len(load_order)
            if length == 2 and not self.is_esl(usable_name):
                if load_order.isalnum():
                    continue
            elif length == 5 and self.is_esl(usable_name):
                if load_order.isalnum():
                    if load_order[:2] in ["FE", "FF"]:
                        continue

            self.errors.append(INCORRECT_LOAD_ORDER)

    def is_esl(self, usable_name):
        variant = self.split_variant(usable_name)
        return variant[2] == "esl"

    def is_valid(self):
        return self.errors == []

    def collect_selected(self):
        selected_from_post = self.data.getlist("selected", [])
        collected = []
        for usable_name in selected_from_post:
            if usable_name == "":
                continue
            variant = self.split_variant(usable_name)
            collected.append({
                "name": self.get_name(usable_name),
                "usable_name": usable_name,
                "version": variant[0],
                "language": variant[1],
                "esl": variant[2],
                "load_order": self.data.get(f"{usable_name}_load_order")
            })
        SelectedPlugins(self.request).set(collected)

    def split_variant(self, usable_name):
        variant = self.request.POST.get(f"{usable_name}_variant")
        return variant.split("&")

    @staticmethod
    def get_name(usable_name):
        plugin = Plugins.objects.get(usable_name=usable_name)
        return plugin.name


class SkillsValidationError(Exception):
    pass


class ValidateSkills:
    def __init__(self, request):
        self.request = request
        self.errors = []
        self.desired_level = self._desired_level_validation()
        self.multiplier = self._priority_multiplier_validation()
        self.fill_skills = self._get_fill_skills()
        self.skills = self.prepare_skills()

    def is_valid(self):
        return self.errors == []

    def _desired_level_validation(self):
        desired_level = self.request.POST.get("desired_level")
        try:
            level = int(desired_level)
            if 81 >= level >= 1:
                return level
            self.errors.append(SKILLS_ERROR_DESIRED_LEVEL_RANGE)
        except ValueError:
            self.errors.append(SKILLS_ERROR_DESIRED_LEVEL)

    def _priority_multiplier_validation(self):
        multiplier = self.request.POST.get("priority_multiplier")
        try:
            return float(multiplier)
        except ValueError:
            self.errors.append(SKILLS_ERROR_MULTIPLIER)

    def prepare_skills(self):
        base_skills = copy.deepcopy(DEFAULT_SKILLS)
        for skills in base_skills.values():
            for skill, properties in skills.items():
                skill_name = properties.get("name")
                default_skill = self._get_default_skill(skill, skill_name)
                desired_skill = self._get_desired_skill(skill, skill_name)
                multiplier = self._get_multiplier(skill)
                if not self.is_new_skill_bigger(default_skill, desired_skill):
                    self.errors.append(SKILLS_ERROR_NEW_VALUE_BIGGER.format(skill=skill_name))
                properties.update({
                  "default_value": default_skill,
                  "desired_value": desired_skill,
                  "multiplier": multiplier
                })
        return base_skills

    @staticmethod
    def is_new_skill_bigger(default_skill, desired_skill):
        try:
            return default_skill <= desired_skill
        except TypeError:
            return True

    def _get_default_skill(self, skill, skill_name):
        try:
            value = int(self.request.POST.get(f"{skill}_base"))
            if 15 <= value <= 100:
                return value
        except ValueError:
            pass
        self.errors.append(SKILLS_ERROR_BASE_SKILL.format(skill=skill_name))

    def _get_desired_skill(self, skill, skill_name):
        value = self.request.POST.get(f"{skill}_new")
        if value == "":
            return value
        try:
            value = int(value)
            if 15 <= value <= 100:
                return value
        except ValueError:
            pass
        self.errors.append(SKILLS_ERROR_DESIRED_SKILL.format(skill=skill_name))

    def _get_multiplier(self, skill):
        multiplier = self.request.POST.get(f"{skill}_multiplier")
        return multiplier == "on"

    def _get_fill_skills(self):
        return self.request.POST.get("fill_skills")

    def save(self):
        if self.is_valid():
            skills = NewSkills(self.request)
            skills.save_skills(self.skills)
            skills.save_desired_level(self.desired_level)
            skills.save_multiplier(self.multiplier)
            skills.save_fill_skills(self.fill_skills)
        else:
            raise SkillsValidationError(self.errors)
