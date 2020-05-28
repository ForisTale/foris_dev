from django.test import TestCase


class CommandsViewTest(TestCase):

    def test_commands_use_template(self):
        response = self.client.get("/the_elder_commands/commands/")
        self.assertTemplateUsed(response, "the_elder_commands/commands.html")

    def test_view_pass_commands_from_other_pages(self):
        session = self.client.session
        session.update({"items_commands": ["player.additem item01 01"], "skills_commands": ["skills"]})
        session.save()

        response = self.client.get("/the_elder_commands/commands/")
        self.assertEqual(response.context["commands"], ["skills", "player.additem item01 01"])
