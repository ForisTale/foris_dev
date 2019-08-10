from django.test import TestCase
from the_elder_commands.forms import CharacterForm
from the_elder_commands.models import Character


class CharacterFormTest(TestCase):

    def test_form_passes_data_to_service(self):
        instance = Character.objects.get_or_create(session_key="key")[0]
        form = CharacterForm(data={"race": "Nord"}, instance=instance)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Character.objects.count(), 1)
        self.assertEqual(
            Character.objects.get(session_key="key"),
            Character.objects.all()[0]
        )
