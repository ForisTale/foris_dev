from django import forms
from the_elder_commands.models import Character


class CharacterForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["race"].required = False
        self.fields["skills"].required = False
        self.fields["desired_level"].required = False
        self.fields["priority_multiplier"].required = False

    class Meta:
        model = Character
        fields = (
            "race", "skills", "desired_level",
            "priority_multiplier",
        )

    def clean_desired_level(self):
        form_data = self.cleaned_data["desired_level"]
        if form_data is not None:
            if form_data < 1 or form_data > 81:
                raise forms.ValidationError("The desired level need to be a integer between 1 and 81.")
        return form_data

    def clean_skills(self):
        form_data = self.cleaned_data["skills"]
        self.ensure_all_skills_are_integers(form_data)
        self.check_skills_range(form_data)
        self.check_desired_is_bigger(form_data)
        return form_data

    @staticmethod
    def check_desired_is_bigger(form_data):
        if form_data is not None:
            for skills in form_data.values():
                for skill in skills.values():
                    if skill["desired_value"] == "":
                        continue
                    default_value = skill["default_value"]
                    if default_value > skill["desired_value"]:
                        raise forms.ValidationError("New value of skills must be bigger than a value!")

    @staticmethod
    def check_skills_range(form_data):
        if form_data is not None:
            for skills in form_data.values():
                for skill in skills.values():
                    for kind in ["default", "desired"]:
                        skill_value = skill[kind + "_value"]
                        if skill_value == "":
                            continue
                        if skill_value < 15 or skill_value > 100:
                            raise forms.ValidationError("The skill need to be a integer between 15 and 100.")

    @staticmethod
    def ensure_all_skills_are_integers(skills_dict):
        if skills_dict is not None:
            for skills in skills_dict.values():
                for skill in skills.values():
                    for kind in ["default", "desired"]:
                        if skill[kind + "_value"] == "":
                            continue
                        try:
                            skill[kind + "_value"] = int(skill[kind + "_value"])
                        except ValueError:
                            raise forms.ValidationError("All skills values must be integers!")
