from django.test import TestCase
from django.test.utils import tag
from django.http import JsonResponse
from the_elder_commands.inventory import COMMANDS_SUCCESS_MESSAGE, ITEMS_COMMANDS_POST_EMPTY_MESSAGE, \
    CONVERT_POST_JS_ERROR, NO_PLUGIN_SELECTED_ERROR_MESSAGE
from the_elder_commands.utils_for_tests import check_test_tag, select_plugin, populate_plugins_table
from the_elder_commands.views import convert_items_post, convert_items_input


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


class ConvertItemsFromPostTest(TestCase):
    def test_convert_post_to_list_of_form_id_and_amount(self):
        class FakeRequest:
            POST = {"table_input": '[{"name":"0101BFEF","value":"1"},{"name":"010282E9","value":"12"},'
                    '{"name":"010282E6","value":""}]'}

        result = convert_items_post(FakeRequest())
        self.assertEqual(result, {"0101BFEF": "1", "010282E9": "12"})

    def test_incorrect_post_give_error_message(self):

        class FakeRequest:
            POST = {}
            session = {"items_messages": []}

        request = FakeRequest()
        output = convert_items_post(request)
        self.assertEqual(request.session.get("items_messages"), [CONVERT_POST_JS_ERROR])
        self.assertEqual(output, {})


class ConvertItemsInputTest(TestCase):
    def test_convert_input(self):
        case = [{"value": "1", "name": "A1"}, {"value": "", "name": "A2"}, {"value": "3", "name": "A3"}]
        result = convert_items_input(case)
        expected = {"A1": "1", "A3": "3"}
        self.assertEqual(expected, result)
