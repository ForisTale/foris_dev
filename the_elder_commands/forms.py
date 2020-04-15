from django.forms.models import ModelForm
from django.forms import ValidationError
from the_elder_commands.models import Character, Plugins, PluginVariants
from the_elder_commands.inventory import ADD_PLUGIN_FILE_ERROR_MESSAGE, PLUGINS_ERROR_NOT_STRING, \
    PLUGINS_ERROR_STRING_IS_EMTPY, PLUGINS_ERROR_NAME_BECOME_EMPTY


class CharacterForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["race"].required = False
        self.fields["skills"].required = False
        self.fields["desired_level"].required = False
        self.fields["priority_multiplier"].required = False
        self.fields["fill_skills"].required = False

    class Meta:
        model = Character
        fields = (
            "race", "skills", "desired_level",
            "priority_multiplier", "fill_skills",
        )

    def clean_desired_level(self):
        form_data = self.cleaned_data["desired_level"]
        if form_data is not None:
            if form_data < 1 or form_data > 81:
                raise ValidationError("The desired level need to be a integer between 1 and 81.")
        return form_data

    def clean_skills(self):
        form_data = self.cleaned_data["skills"]
        if form_data is not None:
            for skills in form_data.values():
                for skill in skills.values():
                    self.ensure_all_skills_are_integers(skill)
                    self.check_skills_range(skill)
                    self.check_desired_is_bigger(skill)
        return form_data

    @staticmethod
    def check_desired_is_bigger(skill):
        if skill["desired_value"] == "":
            return
        if skill["default_value"] > skill["desired_value"]:
            raise ValidationError("New value of skills must be bigger than a value!")

    @staticmethod
    def check_skills_range(skill):
        for kind in ["default", "desired"]:
            skill_value = skill[kind + "_value"]
            if skill_value == "":
                return
            if skill_value < 15 or skill_value > 100:
                raise ValidationError("The skill need to be a integer between 15 and 100.")

    @staticmethod
    def ensure_all_skills_are_integers(skill):
        for kind in ["default", "desired"]:
            if skill[kind + "_value"] == "":
                return
            try:
                skill[kind + "_value"] = int(skill[kind + "_value"])
            except ValueError:
                raise ValidationError("All skills values must be integers!")


class PluginsForm:
    def __init__(self, plugin_name):
        self.plugin_name = plugin_name
        self.errors = []

        if self.is_valid():
            self.plugin_name = self.get_name(plugin_name)
            self.plugin_usable_name = self.get_usable_name()
            self.plugin_instance, created = Plugins.objects.get_or_create(plugin_name=self.plugin_name,
                                                                          plugin_usable_name=self.plugin_usable_name)

    def is_valid(self):
        if isinstance(self.plugin_name, str):
            if self.plugin_name == "":
                self.errors.append(PLUGINS_ERROR_STRING_IS_EMTPY)
                return False
            else:
                if self.name_become_empty():
                    self.errors.append(PLUGINS_ERROR_NAME_BECOME_EMPTY)
                    return False
                else:
                    return True
        else:
            self.errors.append(PLUGINS_ERROR_NOT_STRING)
            return False

    def name_become_empty(self):
        name = self.get_name(self.plugin_name)
        name = name.strip()
        if name == "":
            return True
        else:
            return False

    def get_name(self, raw_name):
        converted = self.cut_special_letters(raw_name)
        return converted

    @staticmethod
    def cut_special_letters(raw_string):
        converted = ""
        for letter in raw_string:
            if letter.isalnum() or letter == " ":
                converted += letter
            else:
                converted += ""
        return converted

    def get_usable_name(self):
        converted = ""
        for letter in self.plugin_name:
            if letter == " ":
                converted += "_"
            else:
                converted += letter.lower()
        return converted


class PluginVariantsForm(ModelForm):
    def __init__(self, plugin_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data["plugin_instance"] = plugin_instance

    class Meta:
        model = PluginVariants
        fields = ("plugin_version", "plugin_language", "plugin_data", "plugin_instance")

        error_messages = {
            "plugin_data": {"required": ADD_PLUGIN_FILE_ERROR_MESSAGE},
        }

    def clean_plugin_data(self):
        plugin_keys = ["WEAP", "ARMO", "BOOK", "INGR", "ALCH", "MISC",
                       "AMMO", "SCRL", "SLGM", "KEYM", "SPEL", "WOOP"]
        form_data = self.cleaned_data["plugin_data"]
        data_keys = form_data.keys()

        if set(plugin_keys).symmetric_difference(data_keys):
            raise ValidationError(ADD_PLUGIN_FILE_ERROR_MESSAGE)

        return form_data
