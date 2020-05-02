from django.test import TestCase
from functional_tests.the_elder_commands import test_plugins
from the_elder_commands.services import ItemsService
from the_elder_commands.inventory import ITEMS_COMMANDS_SUCCESS_MESSAGE, ITEMS_COMMANDS_POST_EMPTY_MESSAGE, \
    ITEMS_CONVERT_POST_ERROR
from the_elder_commands.views import convert_items_post


class ItemsViewTest(TestCase):
    def setUp(self):
        super().setUp()
        test_plugins.AddPluginTest.populate_plugins_table()

    def selected_placeholder(self):
        session = self.client.session
        session.update({"selected": [{
                "name": "test 01",
                "usable_name": "test_01",
                "version": "03",
                "language": "english",
                "load_order": "A5"
            }]})
        session.save()

    def test_items_use_template(self):
        self.selected_placeholder()

        response = self.client.get("/the_elder_commands/items/")
        self.assertTemplateUsed(response, "the_elder_commands/items.html")

    def test_redirect_when_plugin_is_not_selected(self):
        response = self.client.get("/the_elder_commands/items/")
        self.assertRedirects(response, "/the_elder_commands/plugins/")

    def test_view_pass_items_service_to_template(self):
        self.selected_placeholder()

        response = self.client.get("/the_elder_commands/items/")
        self.assertIsInstance(response.context["service"], ItemsService)

    def test_redirect_after_POST(self):
        self.selected_placeholder()
        post = {"table_input": ["00BB00BB=12&00CC00CC="]}
        response = self.client.post("/the_elder_commands/items/", data=post)
        self.assertRedirects(response, "/the_elder_commands/items/")

    def test_view_convert_post_to_console_codes(self):
        cases = {"00AA00AA=&00BB00BB=12&00CC00CC=": ["player.additem 00BB00BB 12"],
                 "00AA00AA=&00BB00BB=&00CC00CC=": []}
        for table_input, expected in cases.items():
            self.selected_placeholder()
            post = {"table_input": [table_input]}
            self.client.post("/the_elder_commands/items/", data=post)
            session = self.client.session
            codes = session.get("items_commands")
            self.assertEqual(codes, expected)

    def test_successful_post_give_message_to_view(self):
        self.selected_placeholder()
        post = {"table_input": ["00AA00AA=1"]}
        response = self.client.post("/the_elder_commands/items/", data=post)
        self.assertEqual(response.json().get("message"), ITEMS_COMMANDS_SUCCESS_MESSAGE)

    def test_give_empty_post_message_after_empty_POST(self):
        self.selected_placeholder()
        post = {"table_input": ["00AA00AA=&00BB00BB=&00CC00CC="]}
        response = self.client.post("/the_elder_commands/items/", data=post)
        self.assertEqual(response.json().get("message"), ITEMS_COMMANDS_POST_EMPTY_MESSAGE)


class ConvertItemsPostTest(TestCase):
    def test_convert_post_to_list_of_formid_and_amount(self):

        class FakeRequest:
            POST = {"table_input": "00AA00AA=1&00BB00BB=12&00CC00CC="}

        result = convert_items_post(FakeRequest())
        self.assertEqual(result, ["player.additem 00AA00AA 1", "player.additem 00BB00BB 12"])

    def test_incorrect_post_give_error_message(self):

        class FakeRequest:
            POST = {}
            session = {"items_messages": []}

        request = FakeRequest()
        convert_items_post(request)
        self.assertEqual(request.session.get("items_messages"), [ITEMS_CONVERT_POST_ERROR])

