from django.test import TestCase
from django.test.utils import tag
from django.http import JsonResponse
from the_elder_commands.utils_for_tests.populate_plugins_table import populate_plugins_table
from the_elder_commands.utils_for_tests.check_test_tag import check_test_tag
from the_elder_commands.utils_for_tests.select_plugin import select_plugin
from the_elder_commands.inventory.messages import NO_PLUGIN_SELECTED_ERROR_MESSAGE, COMMANDS_SUCCESS_MESSAGE, \
    SPELLS_COMMANDS_POST_EMPTY_MESSAGE


class SpellsViewTest(TestCase):

    def setUp(self):
        populate_plugins_table()

        if check_test_tag(self, "dont_select"):
            pass
        else:
            select_plugin(self)

        self.base_url = "/the_elder_commands/spells/"

    def test_view_use_template(self):
        response = self.client.get(self.base_url)
        self.assertTemplateUsed(response, "the_elder_commands/spells.html")

    @tag("dont_select")
    def test_redirect_when_plugin_not_selected(self):
        response = self.client.get(self.base_url)
        self.assertRedirects(response, "/the_elder_commands/plugins/")

    @tag("dont_select")
    def test_not_selected_give_error_message(self):
        self.client.get(self.base_url)
        session = self.client.session
        self.assertEqual(session.get("plugins_messages"), [NO_PLUGIN_SELECTED_ERROR_MESSAGE])

    def test_return_json_response_after_post(self):
        post = {"table_input": ['[{"name":"010282E9","value":"12"}]']}
        response = self.client.post(self.base_url, data=post)
        self.assertIsInstance(response, JsonResponse)

    def test_view_convert_post(self):
        cases = {'[{"name":"010282E9","value":"on"}]': [{"010282E9": "on"}, ["player.addspell 010282E9"]],
                 '[{"name":"010282E9","value":""}]': [{}, []]}
        for table_input, expected in cases.items():
            post = {"table_input": [table_input]}
            self.client.post(self.base_url, data=post)
            session = self.client.session
            chosen = session.get("chosen_spells")
            self.assertEqual(chosen, expected[0], msg=f"Fail on: {table_input}")
            codes = session.get("spells_commands")
            self.assertEqual(codes, expected[1], msg=f"Fail on: {table_input}")

    def test_successful_post_give_message_to_view(self):
        post = {"table_input": ['[{"name":"0101BFEF","value":"on"},{"name":"010282E9","value":"on"}]']}
        response = self.client.post(self.base_url, data=post)
        self.assertIn(COMMANDS_SUCCESS_MESSAGE, response.json().get("message"))

    def test_give_empty_post_message_after_empty_POST(self):
        post = {"table_input": ['[{"name":"0101BFEF","value":""},{"name":"010282E9","value":""}]']}
        response = self.client.post(self.base_url, data=post)
        self.assertIn(SPELLS_COMMANDS_POST_EMPTY_MESSAGE, response.json().get("message"))

    def test_reset_post_return_json_response(self):
        response = self.client.post(self.base_url, {"reset": ""})
        self.assertIsInstance(response, JsonResponse)

    def test_reset_post_clear_chosen_and_commands(self):
        session = self.client.session
        session.update({"chosen_spells": {"some": 1}, "spells_commands": ["some commands"]})
        session.save()
        self.client.post(self.base_url, {"reset": ""})

        session = self.client.session
        self.assertEqual(session.get("chosen_spells"), {})
        self.assertEqual(session.get("spells_commands"), [])
