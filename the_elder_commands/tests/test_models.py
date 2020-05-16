from django.test import TestCase
from the_elder_commands.models import Character, Plugins, PluginVariants
from django.db import IntegrityError


class CharacterModelTest(TestCase):

    def test_model_has_default_value_for_race(self):
        character = Character()
        self.assertEqual(character.race, "Nord")

    def test_session_key_is_unique(self):
        Character.objects.create(session_key="key")

        with self.assertRaises(IntegrityError):
            Character.objects.create(session_key="key")


class PluginsModelTest(TestCase):

    def test_name_is_unique(self):
        Plugins.objects.create(name="test")
        with self.assertRaises(IntegrityError):
            Plugins.objects.create(name="test")


class PluginVariantsTest(TestCase):

    def test_version_and_language_are_unique_for_plugin(self):
        plugin = Plugins.objects.create(name="test", usable_name="test")
        PluginVariants.objects.create(language="English", version="0.1", instance=plugin, esl=True)
        PluginVariants.objects.create(language="English", version="0.1", instance=plugin, esl=False)
        PluginVariants.objects.create(language="English", version="0.2", instance=plugin, esl=True)

        other_plugin = Plugins.objects.create(name="test 2", usable_name="test_2")
        PluginVariants.objects.create(language="English", version="0.1",
                                      instance=other_plugin, esl=True)  # should not raise

        with self.assertRaises(IntegrityError):
            PluginVariants.objects.create(language="English", version="0.1", instance=plugin, esl=True)
