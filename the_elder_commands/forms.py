from django import forms
from the_elder_commands.models import Character


class CharacterForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["race"].required = False
        self.fields["default_skills"].required = False
        self.fields["desired_skills"].required = False

    class Meta:
        model = Character
        fields = ("race", "default_skills", "desired_skills")
