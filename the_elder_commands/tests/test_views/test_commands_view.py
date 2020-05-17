from django.test import TestCase
from the_elder_commands.views import create_items_commands


class CommandsViewTest(TestCase):

    def test_commands_use_template(self):
        response = self.client.get("/the_elder_commands/commands/")
        self.assertTemplateUsed(response, "the_elder_commands/commands.html")

    def test_view_pass_commands_from_other_pages(self):
        session = self.client.session
        session.update({"chosen_items": {"item01": "01", "item02": "02"}, "skills_commands": ["skills"]})
        session.save()

        response = self.client.get("/the_elder_commands/commands/")
        self.assertEqual(response.context["commands"], ["skills", "player.additem item01 01",
                                                        "player.additem item02 02"])


class CreateItemsCommandsTest(TestCase):

    def test_return_list_of_commands(self):

        class FakeRequest:
            session = {"chosen_items": {"item01": "01", "item02": "02"}}

        actual = create_items_commands(FakeRequest)
        expected = ["player.additem item01 01", "player.additem item02 02"]
        self.assertEqual(actual, expected)

    def test_return_empty_list_when_no_commands(self):
        class FakeRequest:
            session = {}
        self.assertEqual(create_items_commands(FakeRequest), [])


