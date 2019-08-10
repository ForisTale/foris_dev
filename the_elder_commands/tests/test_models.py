from django.test import TestCase
from the_elder_commands.models import Character
from django.db import IntegrityError


class CharacterModelTest(TestCase):

    def test_model_has_default_value_for_race(self):
        character = Character()
        self.assertEqual(character.race, "Nord")

    def test_session_key_is_unique(self):
        Character.objects.create(session_key="key")

        with self.assertRaises(IntegrityError):
            Character.objects.create(session_key="key")
