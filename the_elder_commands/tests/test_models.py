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
        Plugins.objects.create(plugin_name="test")
        with self.assertRaises(IntegrityError):
            Plugins.objects.create(plugin_name="test")


class PluginVariantsTest(TestCase):

    def test_version_and_language_are_unique_for_plugin(self):
        plugin = Plugins.objects.create(plugin_name="test", plugin_usable_name="test")
        PluginVariants.objects.create(plugin_language="English", plugin_version="0.1", plugin_instance=plugin)
        PluginVariants.objects.create(plugin_language="English", plugin_version="0.2", plugin_instance=plugin)

        other_plugin = Plugins.objects.create(plugin_name="test 2", plugin_usable_name="test_2")
        PluginVariants.objects.create(plugin_language="English", plugin_version="0.1",
                                      plugin_instance=other_plugin)  # should not raise

        with self.assertRaises(IntegrityError):
            PluginVariants.objects.create(plugin_language="English", plugin_version="0.1", plugin_instance=plugin)
