from django.forms.models import ModelForm
from django.forms import ValidationError, FileInput
from the_elder_commands.models import Character, Plugins
from the_elder_commands.inventory import ADD_PLUGIN_FILE_ERROR_MESSAGE


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


class AddPluginsForm(ModelForm):
    class Meta:
        model = Plugins
        fields = ("plugin_name", "plugin_usable_name", "plugin_version", "plugin_language", "plugin_data")
        error_messages = {
            "plugin_data": {"required": ADD_PLUGIN_FILE_ERROR_MESSAGE}
        }

    def clean_plugin_data(self):
        plugin_keys = ["WEAP", "ARMO", "BOOK", "INGR", "ALCH", "MISC",
                       "AMMO", "SCRL", "SLGM", "KEYM", "SPEL", "WOOP"]
        form_data = self.cleaned_data["plugin_data"]
        data_keys = form_data.keys()

        if set(plugin_keys).symmetric_difference(data_keys):
            raise ValidationError(ADD_PLUGIN_FILE_ERROR_MESSAGE)

        return form_data

