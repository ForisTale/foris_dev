from django.test import TestCase
from the_elder_commands.models import Plugins, PluginVariants
from django.db import IntegrityError


class PluginsModelTest(TestCase):

    def test_name_is_unique(self):
        Plugins.objects.create(name="test")
        with self.assertRaises(IntegrityError):
            Plugins.objects.create(name="test")


class PluginVariantsTest(TestCase):

    def test_version_and_language_are_unique_for_plugin(self):
        plugin = Plugins.objects.create(name="test", usable_name="test")
        PluginVariants.objects.create(language="English", version="0.1", instance=plugin, is_esl=True)
        PluginVariants.objects.create(language="English", version="0.1", instance=plugin, is_esl=False)
        PluginVariants.objects.create(language="English", version="0.2", instance=plugin, is_esl=True)

        other_plugin = Plugins.objects.create(name="test 2", usable_name="test_2")
        PluginVariants.objects.create(language="English", version="0.1",
                                      instance=other_plugin, is_esl=True)  # should not raise

        with self.assertRaises(IntegrityError):
            PluginVariants.objects.create(language="English", version="0.1", instance=plugin, is_esl=True)
