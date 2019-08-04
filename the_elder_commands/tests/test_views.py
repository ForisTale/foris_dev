from django.test import TestCase
from the_elder_commands.forms import CharacterForm


class CharacterViewTest(TestCase):

    def test_tec_use_template(self):
        response = self.client.get("/the_elder_commands/")
        self.assertTemplateUsed(response, "the_elder_commands/character.html")

    def test_character_view_use_form(self):
        response = self.client.get("/the_elder_commands/")
        self.assertIsInstance(
            response.context["character_form"],
            CharacterForm
        )

