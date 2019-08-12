from django import forms
from the_elder_commands.models import Character


class CharacterForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["race"].required = False
        self.fields["default_skills"].required = False
        self.fields["desired_skills"].required = False
        self.fields["desired_level"].required = False
        self.fields["priority_multiplier"].required = False

    class Meta:
        model = Character
        fields = (
            "race", "default_skills", "desired_skills",
            "desired_level", "priority_multiplier",
        )

    def clean_desired_level(self):
        form_data = self.cleaned_data["desired_level"]
        if form_data is not None:
            if form_data < 1 or form_data > 81:
                raise forms.ValidationError("The desired level need to be a integer between 1 and 81.")
        return form_data

    def clean_default_skills(self):
        form_data = self.cleaned_data["default_skills"]
        self.ensure_all_skills_are_integers(form_data)
        self.check_skills_range(form_data)
        return form_data

    def clean_desired_skills(self):
        form_data = self.cleaned_data["desired_skills"]
        self.ensure_all_skills_are_integers(form_data)
        self.check_skills_range(form_data)
        return form_data

    def clean(self):
        form_data = self.cleaned_data
        try:
            default_skills = form_data["default_skills"]
            desired_skills = form_data["desired_skills"]
        except KeyError:
            return form_data
        if default_skills and desired_skills:
            for category, skills in desired_skills.items():
                for name, skill in skills.items():
                    if skill["value"] == "":
                        continue
                    default_value = default_skills[category][name]["value"]
                    if default_value > skill["value"]:
                        raise forms.ValidationError("New value of skills must be bigger than a value!")
        return form_data

    @staticmethod
    def check_skills_range(skills_dict):
        if skills_dict is not None:
            for skills in skills_dict.values():
                for skill in skills.values():
                    if skill["value"] == "":
                        continue
                    skill_value = skill["value"]
                    if skill_value < 15 or skill_value > 100:
                        raise forms.ValidationError("The skill need to be a integer between 15 and 100.")

    @staticmethod
    def ensure_all_skills_are_integers(skills_dict):
        if skills_dict is not None:
            for skills in skills_dict.values():
                for skill in skills.values():
                    if skill["value"] == "":
                        continue
                    try:
                        skill["value"] = int(skill["value"])
                    except ValueError:
                        raise forms.ValidationError("All skills value must be integers!")
