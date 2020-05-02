from django.forms.models import ModelForm
from django.forms import ValidationError
from the_elder_commands.models import Character, Plugins, PluginVariants
from the_elder_commands.inventory import ADD_PLUGIN_FILE_ERROR_MESSAGE, INCORRECT_LOAD_ORDER, \
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
        if form_data is None:
            return 1
        else:
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
    def __init__(self, name):
        self.name = name
        self.errors = []

        self.clean_name()
        if self.is_valid():
            self.name = self.get_name(name)
            self.usable_name = self.get_usable_name()
            self.instance, created = Plugins.objects.get_or_create(name=self.name,
                                                                   usable_name=self.usable_name)

    def clean_name(self):
        if self.name == "":
            self.errors.append(PLUGINS_ERROR_STRING_IS_EMTPY)
        else:
            if self.name_become_empty():
                self.errors.append(PLUGINS_ERROR_NAME_BECOME_EMPTY)

    def is_valid(self):
        return self.errors == []

    def name_become_empty(self):
        name = self.get_name(self.name)
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
        for letter in self.name:
            if letter == " ":
                converted += "_"
            else:
                converted += letter.lower()
        return converted


class PluginVariantsForm(ModelForm):
    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data["instance"] = instance

    class Meta:
        model = PluginVariants
        fields = ("version", "language", "plugin_data", "instance")

        error_messages = {
            "plugin_data": {"required": ADD_PLUGIN_FILE_ERROR_MESSAGE},
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
        plugin_keys = ["WEAP", "ARMO", "BOOK", "INGR", "ALCH", "MISC",
                       "AMMO", "SCRL", "SLGM", "KEYM", "SPEL", "WOOP"]
        form_data = self.cleaned_data["plugin_data"]
        data_keys = form_data.keys()

        if set(plugin_keys).symmetric_difference(data_keys):
            raise ValidationError(ADD_PLUGIN_FILE_ERROR_MESSAGE)

        return form_data


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
            load_order = self.data.get(f"{usable_name}_load_order", "")
            length = len(load_order)
            if length == 2 or length == 5:
                if load_order.isalnum():
                    return
                else:
                    self.errors.append(INCORRECT_LOAD_ORDER)
                    return
            else:
                self.errors.append(INCORRECT_LOAD_ORDER)
                return

    def is_valid(self):
        return self.errors == []

    def collect_selected(self):
        selected = self.data.getlist("selected", [])
        collected = []
        for usable_name in selected:
            collected.append({
                "name": self.get_name(usable_name),
                "usable_name": usable_name,
                "version": self.get_version(usable_name),
                "language": self.get_language(usable_name),
                "load_order": self.data.get(f"{usable_name}_load_order")
            })
        self.request.session.update({"selected": collected})

    def get_version(self, usable_name):
        variant = self.request.POST.get(f"{usable_name}_variant")
        version = variant[:variant.find("&")]
        return version

    def get_language(self, usable_name):
        variant = self.request.POST.get(f"{usable_name}_variant")
        language = variant[variant.find("&") + 1:]
        return language

    @staticmethod
    def get_name(usable_name):
        plugin = Plugins.objects.get(usable_name=usable_name)
        return plugin.name
