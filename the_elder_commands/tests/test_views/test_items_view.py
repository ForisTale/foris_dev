from django.test import TestCase
from django.test.utils import tag
from django.http import JsonResponse
from the_elder_commands.inventory.messages import COMMANDS_SUCCESS_MESSAGE, ITEMS_COMMANDS_POST_EMPTY_MESSAGE, \
    NO_PLUGIN_SELECTED_ERROR_MESSAGE
from the_elder_commands.utils_for_tests.populate_plugins_table import populate_plugins_table
from the_elder_commands.utils_for_tests.check_test_tag import check_test_tag
from the_elder_commands.utils_for_tests.select_plugin import select_plugin


class ItemsViewTest(TestCase):
    def setUp(self):
        populate_plugins_table()

        if check_test_tag(self, "dont_select_plugin"):
            pass
        else:
            select_plugin(self)

        self.base_url = "/the_elder_commands/items/"

    def test_items_use_template(self):

        response = self.client.get(self.base_url)
        self.assertTemplateUsed(response, "the_elder_commands/items.html")

    @tag("dont_select_plugin")
    def test_redirect_when_plugin_is_not_selected(self):
        response = self.client.get(self.base_url)
        self.assertRedirects(response, "/the_elder_commands/plugins/")

    @tag("dont_select_plugin")
    def test_not_selected_give_error_message(self):
        self.client.get(self.base_url)
        session = self.client.session
        self.assertEqual(session.get("plugins_messages"), [NO_PLUGIN_SELECTED_ERROR_MESSAGE])

    def test_return_json_response_after_post(self):
        post = {"table_input": ['[{"name":"010282E9","value":"12"}]']}
        response = self.client.post(self.base_url, data=post)
        self.assertIsInstance(response, JsonResponse)

    def test_view_convert_post_to_console_codes(self):
        cases = {'[{"name":"010282E9","value":"12"}]': [{"010282E9": "12"}, ['player.additem 010282E9 12']],
                 '[{"name":"010282E9","value":""}]': [{}, []]}
        for table_input, expected in cases.items():
            post = {"table_input": [table_input]}
            self.client.post(self.base_url, data=post)
            session = self.client.session
            chosen = session.get("chosen_items")
            self.assertEqual(chosen, expected[0], msg=f"Fail on: {chosen}")
            codes = session.get("items_commands")
            self.assertEqual(codes, expected[1], msg=f"Fail on: {codes}")

    def test_successful_post_give_message_to_view(self):
        post = {"table_input": ['[{"name":"0101BFEF","value":"1"},{"name":"010282E9","value":"12"}]']}
        response = self.client.post(self.base_url, data=post)
        self.assertIn(COMMANDS_SUCCESS_MESSAGE, response.json().get("message"))

    def test_give_empty_post_message_after_empty_POST(self):
        post = {"table_input": ['[{"name":"0101BFEF","value":""},{"name":"010282E9","value":""}, '
                                '{"name":"010282E6","value":""}]']}
        response = self.client.post(self.base_url, data=post)
        self.assertIn(ITEMS_COMMANDS_POST_EMPTY_MESSAGE, response.json().get("message"))

    def test_reset_post_return_json_response(self):
        response = self.client.post(self.base_url, {"reset": ""})
        self.assertIsInstance(response, JsonResponse)

    def test_reset_post_clear_chosen_and_commands(self):
        session = self.client.session
        session.update({"chosen_items": {"some": 1}, "items_commands": ["some commands"]})
        session.save()
        self.client.post(self.base_url, {"reset": ""})

        session = self.client.session
        self.assertEqual(session.get("chosen_items"), {})
        self.assertEqual(session.get("items_commands"), [])
