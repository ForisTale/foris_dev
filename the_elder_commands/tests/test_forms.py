from django.test import TestCase
from the_elder_commands.forms import CharacterForm
from the_elder_commands.models import Character


class CharacterFormTest(TestCase):

    def test_form_passes_data_to_service(self):
        form = CharacterForm(data={"race": "Nord", "session_key": "key"})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Character.objects.count(), 1)
        self.assertEqual(
            Character.objects.get(session_key="key"),
            Character.objects.all()[0]
        )

    def test_session_key_is_required(self):
        form = CharacterForm(data={"session_key": ""})
        self.assertEqual(
            form.errors["session_key"],
            ["This field is required."]
        )
