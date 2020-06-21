from django.forms.models import ModelForm
from django.http import QueryDict
from django.forms import ValidationError
from the_elder_commands.models import Plugins, PluginVariants, Weapons, WordsOfPower, Keys, Books, Perks, Ammo, \
    Armors, Alchemy, Miscellaneous, Ingredients, Scrolls, SoulsGems, AlterationSpells, OtherSpells, ConjurationSpells,\
    DestructionSpells, IllusionSpells, RestorationSpells
from the_elder_commands.inventory import ADD_PLUGIN_ERROR_FILE, INCORRECT_LOAD_ORDER, \
    PLUGINS_ERROR_NAME_IS_EMTPY, PLUGINS_ERROR_NAME_BECOME_EMPTY, \
    SKILLS_ERROR_NEW_VALUE_BIGGER, SKILLS_ERROR_DESIRED_LEVEL_RANGE, \
    SKILLS_ERROR_DESIRED_LEVEL, SKILLS_ERROR_MULTIPLIER, DEFAULT_SKILLS, SKILLS_ERROR_DESIRED_SKILL, \
    SKILLS_ERROR_BASE_SKILL, ADD_PLUGIN_ERROR_PLUGIN_EXIST
from the_elder_commands.utils import SelectedPlugins, Skills, escape_html
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
                    variant = form.save()
                    self.handle_data_forms(correct_post, variant)
                else:
                    self.variants_form_not_valid(form)
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

    def handle_data_forms(self, post, variant):
        data = post.get("plugin_data", {})
        if self.all_items_are_empty(data):
            self.forms_not_valid(variant)
            return
        forms = [WeaponsForm({"items": data.get("WEAP"), "variant": variant}),
                 ArmorsForm({"items": data.get("ARMO"), "variant": variant}),
                 BooksForm({"items": data.get("BOOK"), "variant": variant}),
                 IngredientsForm({"items": data.get("INGR"), "variant": variant}),
                 AlchemyForm({"items": data.get("ALCH"), "variant": variant}),
                 MiscellaneousForm({"items": data.get("MISC"), "variant": variant}),
                 PerksForm({"perks": data.get("PERK"), "variant": variant}),
                 AmmoForm({"items": data.get("AMMO"), "variant": variant}),
                 ScrollsForm({"items": data.get("SCRL"), "variant": variant}),
                 SoulsGemsForm({"items": data.get("SLGM"), "variant": variant}),
                 KeysForm({"items": data.get("KEYM"), "variant": variant}),
                 SpellsForm({"spells": data.get("SPEL"), "variant": variant}),
                 WordsOfPowerForm({"words": data.get("WOOP"), "variant": variant})]
        are_valid = all(form.is_valid() for form in forms)
        if are_valid:
            [form.save() for form in forms]
        else:
            self.forms_not_valid(variant)

    @staticmethod
    def all_items_are_empty(plugin_data):
        keys = ["WEAP", "ARMO", "BOOK", "INGR", "ALCH", "MISC", "PERK", "AMMO", "SCRL", "SLGM", "KEYM", "SPEL", "WOOP"]
        return all(True if plugin_data.get(key) is None or plugin_data.get(key) == [] else False for key in keys)

    def forms_not_valid(self, variant):
        self.errors.append(ADD_PLUGIN_ERROR_FILE)
        variant.delete()

    def variants_form_not_valid(self, form):
        for header, error in form.errors.items():
            if header == "__all__":
                self.errors.append(ADD_PLUGIN_ERROR_PLUGIN_EXIST)
            else:
                self.errors.append([*error])


class PluginVariantsForm(ModelForm):

    class Meta:
        model = PluginVariants
        fields = ("version", "language", "instance", "is_esl")

    def clean_version(self):
        form_data = self.cleaned_data["version"]
        new_version = ""
        for letter in form_data:
            if letter.isalnum():
                new_version += letter
            elif letter in "_-;:,.":
                new_version += letter

        return new_version


class BaseItemsForm(ModelForm):
    def clean_items(self):
        data = get_cleaned_data(self, "items")
        correct_data = []
        for item in data:
            correct_data.append(self.get_item_data(item))
        return correct_data

    @staticmethod
    def get_item_data(item):
        pass


def get_cleaned_data(self, field_name):
    data = self.cleaned_data[field_name]
    if data is None:
        data = list()
    elif type(data) is not list:
        raise ValidationError("")
    return data


class WeaponsForm(BaseItemsForm):
    class Meta:
        model = Weapons
        fields = ("items", "variant")

    @staticmethod
    def get_item_data(item):
        return {
            "name": get_data(item, "fullName"),
            "editor_id": get_data(item, "editorId"),
            "form_id": get_data(item, "formId"),
            "weight": get_data(item, "Weight"),
            "value": get_data(item, "Value"),
            "damage": get_data(item, "Damage"),
            "type": get_data(item, "Type"),
            "description": get_data(item, "Description"),
        }


class ArmorsForm(BaseItemsForm):
    class Meta:
        model = Armors
        fields = ("items", "variant")

    @staticmethod
    def get_item_data(item):
        return {
                "name": get_data(item, "fullName"),
                "editor_id": get_data(item, "editorId"),
                "form_id": get_data(item, "formId"),
                "weight": get_data(item, "Weight"),
                "value": get_data(item, "Value"),
                "armor_rating": get_data(item, "Armor rating"),
                "armor_type": get_data(item, "Armor type"),
                "description": get_data(item, "Description"),
        }


# noinspection DuplicatedCode
class BooksForm(BaseItemsForm):
    class Meta:
        model = Books
        fields = ("variant", "items")

    @staticmethod
    def get_item_data(item):
        return {
                "name": get_data(item, "fullName"),
                "editor_id": get_data(item, "editorId"),
                "form_id": get_data(item, "formId"),
                "weight": get_data(item, "Weight"),
                "value": get_data(item, "Value"),
        }


# noinspection DuplicatedCode
class IngredientsForm(BaseItemsForm):
    class Meta:
        model = Ingredients
        fields = ("variant", "items")

    @staticmethod
    def get_item_data(item):
        return {
                "name": get_data(item, "fullName"),
                "editor_id": get_data(item, "editorId"),
                "form_id": get_data(item, "formId"),
                "weight": get_data(item, "Weight"),
                "value": get_data(item, "Value"),
                "effects": get_data(item, "Effects"),
        }


# noinspection DuplicatedCode
class AlchemyForm(BaseItemsForm):
    class Meta:
        model = Alchemy
        fields = ("variant", "items")

    @staticmethod
    def get_item_data(item):
        return {
                "name": get_data(item, "fullName"),
                "editor_id": get_data(item, "editorId"),
                "form_id": get_data(item, "formId"),
                "weight": get_data(item, "Weight"),
                "value": get_data(item, "Value"),
                "effects": get_data(item, "Effects"),
        }


class MiscellaneousForm(BaseItemsForm):
    class Meta:
        model = Miscellaneous
        fields = ("variant", "items")

    @staticmethod
    def get_item_data(item):
        return {
                "name": get_data(item, "fullName"),
                "editor_id": get_data(item, "editorId"),
                "form_id": get_data(item, "formId"),
                "weight": get_data(item, "Weight"),
                "value": get_data(item, "Value"),
        }


class AmmoForm(BaseItemsForm):
    class Meta:
        model = Ammo
        fields = ("variant", "items")

    @staticmethod
    def get_item_data(item):
        return {
                "name": get_data(item, "fullName"),
                "editor_id": get_data(item, "editorId"),
                "form_id": get_data(item, "formId"),
                "weight": get_data(item, "Weight"),
                "value": get_data(item, "Value"),
                "damage": get_data(item, "Damage"),
        }


# noinspection DuplicatedCode
class ScrollsForm(BaseItemsForm):
    class Meta:
        model = Scrolls
        fields = ("variant", "items")

    @staticmethod
    def get_item_data(item):
        return {
                "name": get_data(item, "fullName"),
                "editor_id": get_data(item, "editorId"),
                "form_id": get_data(item, "formId"),
                "weight": get_data(item, "Weight"),
                "value": get_data(item, "Value"),
                "effects": get_data(item, "Effects"),
        }


class SoulsGemsForm(BaseItemsForm):
    class Meta:
        model = SoulsGems
        fields = ("variant", "items")

    @staticmethod
    def get_item_data(item):
        return {
                "name": get_data(item, "fullName"),
                "editor_id": get_data(item, "editorId"),
                "form_id": get_data(item, "formId"),
                "weight": get_data(item, "Weight"),
                "value": get_data(item, "Value"),
        }


# noinspection DuplicatedCode
class KeysForm(BaseItemsForm):
    class Meta:
        model = Keys
        fields = ("variant", "items")

    @staticmethod
    def get_item_data(item):
        return {
                "name": get_data(item, "fullName"),
                "editor_id": get_data(item, "editorId"),
                "form_id": get_data(item, "formId"),
                "weight": get_data(item, "Weight"),
                "value": get_data(item, "Value"),
        }


class PerksForm(BaseItemsForm):
    class Meta:
        model = Perks
        fields = ("variant", "perks")

    def clean_perks(self):
        data = get_cleaned_data(self, "perks")
        correct_data = []
        for item in data:
            correct_data.append({
                "name": get_data(item, "fullName"),
                "editor_id": get_data(item, "editorId"),
                "form_id": get_data(item, "formId"),
                "description": get_data(item, "Description"),
            })
        return correct_data


class WordsOfPowerForm(ModelForm):
    class Meta:
        model = WordsOfPower
        fields = ("variant", "words")

    def clean_words(self):
        data = get_cleaned_data(self, "words")
        correct_data = []
        for item in data:
            correct_data.append({
                "name": get_data(item, "fullName"),
                "editor_id": get_data(item, "editorId"),
                "form_id": get_data(item, "formId"),
                "translation": get_data(item, "Translation"),
            })
        return correct_data


class SpellsForm:
    def __init__(self, data):
        sorted_spells = self.sort_spells(data.get("spells"))
        self.forms = self.assign_forms(sorted_spells, data.get("variant"))

    @staticmethod
    def sort_spells(spells):
        if spells is None:
            return {}
        after_sort = {}
        for spell in spells:
            spell_category = spell.get("Category")
            if spell_category == "Alteration":
                after_sort.setdefault("alteration", []).append(spell)
            elif spell_category == "Conjuration":
                after_sort.setdefault("conjuration", []).append(spell)
            elif spell_category == "Destruction":
                after_sort.setdefault("destruction", []).append(spell)
            elif spell_category == "Illusion":
                after_sort.setdefault("illusion", []).append(spell)
            elif spell_category == "Restoration":
                after_sort.setdefault("restoration", []).append(spell)
            else:
                after_sort.setdefault("other", []).append(spell)
        return after_sort

    @staticmethod
    def assign_forms(sorted_spells, variant):
        forms = [
            AlterationSpellsForm({"spells": sorted_spells.get("alteration"), "variant": variant}),
            ConjurationSpellsForm({"spells": sorted_spells.get("conjuration"), "variant": variant}),
            DestructionSpellsForm({"spells": sorted_spells.get("destruction"), "variant": variant}),
            IllusionSpellsForm({"spells": sorted_spells.get("illusion"), "variant": variant}),
            RestorationSpellsForm({"spells": sorted_spells.get("restoration"), "variant": variant}),
            OtherSpellsForm({"spells": sorted_spells.get("other"), "variant": variant})
        ]

        return forms

    def is_valid(self):
        return all(form.is_valid() for form in self.forms)

    def save(self):
        [form.save() for form in self.forms]


class BaseSpellForm(ModelForm):
    def clean_spells(self):
        data = get_cleaned_data(self, "spells")
        correct_data = []
        for item in data:
            correct_data.append({
                "name": get_data(item, "fullName"),
                "editor_id": get_data(item, "editorId"),
                "form_id": get_data(item, "formId"),
                "effects": get_data(item, "Effects"),
                "mastery": get_data(item, "Mastery"),
            })
        return correct_data


# noinspection DuplicatedCode
class AlterationSpellsForm(BaseSpellForm):
    class Meta:
        model = AlterationSpells
        fields = ("variant", "spells")


# noinspection DuplicatedCode
class ConjurationSpellsForm(BaseSpellForm):
    class Meta:
        model = ConjurationSpells
        fields = ("variant", "spells")


# noinspection DuplicatedCode
class DestructionSpellsForm(BaseSpellForm):
    class Meta:
        model = DestructionSpells
        fields = ("variant", "spells")


# noinspection DuplicatedCode
class RestorationSpellsForm(BaseSpellForm):
    class Meta:
        model = RestorationSpells
        fields = ("variant", "spells")


# noinspection DuplicatedCode
class IllusionSpellsForm(BaseSpellForm):
    class Meta:
        model = IllusionSpells
        fields = ("variant", "spells")


# noinspection DuplicatedCode
class OtherSpellsForm(BaseSpellForm):
    class Meta:
        model = OtherSpells
        fields = ("variant", "spells")


def escape_html_for_forms(value):
    if type(value) in [str, int, float]:
        return escape_html(str(value))
    else:
        raise ValidationError("")


def get_data(item, item_key):
    try:
        value = item.get(item_key)
    except AttributeError:
        raise ValidationError("")
    return escape_html_for_forms(value)


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
            skills = Skills(self.request)
            skills.save_skills(self.skills)
            skills.save_desired_level(self.desired_level)
            skills.save_multiplier(self.multiplier)
            skills.save_fill_skills(self.fill_skills)
        else:
            raise SkillsValidationError(self.errors)
