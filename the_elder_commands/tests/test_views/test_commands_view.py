from django.test import TestCase


class CommandsViewTest(TestCase):

    def test_commands_use_template(self):
        response = self.client.get("/the_elder_commands/commands/")
        self.assertTemplateUsed(response, "the_elder_commands/commands.html")

    def test_view_pass_commands_from_other_pages(self):
        session = self.client.session
        session.update({"items_commands": ["item 01", "item 02"], "character_commands": ["character"]})
        session.save()

        response = self.client.get("/the_elder_commands/commands/")
        self.assertEqual(response.context["commands"], ["character", "item 01", "item 02"])



