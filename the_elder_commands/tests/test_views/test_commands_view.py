from django.test import TestCase
from django.http import FileResponse


class CommandsViewTest(TestCase):
    base_url = "/the_elder_commands/commands/"

    def test_commands_use_template(self):
        response = self.client.get(self.base_url)
        self.assertTemplateUsed(response, "the_elder_commands/commands.html")

    def test_view_pass_commands_from_other_pages(self):
        session = self.client.session
        session.update({"items_commands": ["player.additem item01 01"], "skills_commands": ["skills"]})
        session.save()

        response = self.client.get(self.base_url)
        self.assertEqual(response.context["commands"], ["skills", "player.additem item01 01"])


class CommandsDownloadTest(TestCase):
    base_url = "/the_elder_commands/commands/download"

    def test_commands_return_file_response(self):
        response = self.client.get(self.base_url)
        self.assertIsInstance(response, FileResponse)

    def test_response_properties(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="TEC_Commands.txt"')

    def test_correct_file_content(self):
        session = self.client.session
        session.update({"items_commands": ["player.additem item01 01"], "skills_commands": ["skills"]})
        session.save()

        response = self.client.get(self.base_url)
        content = response.streaming_content
        new_list = list(content)
        commands = new_list[0]
        self.assertEqual("skills\nplayer.additem item01 01", commands.decode("utf-8"))
