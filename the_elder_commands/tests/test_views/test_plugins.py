from django.test import TestCase
from django.test.utils import tag
from django.http import QueryDict
from the_elder_commands.models import Plugins, PluginVariants
from the_elder_commands.inventory import ManageTestFiles, ADD_PLUGIN_SUCCESS_MESSAGE, \
    PLUGIN_TEST_FILE, PLUGIN_TEST_DICT, ADD_PLUGIN_FILE_ERROR_MESSAGE
from unittest.mock import patch


class PluginsViewTest(TestCase, ManageTestFiles):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ManageTestFiles.__init__(self)

    def setUp(self):
        super().setUp()

        if self.check_test_tag("create_test_file"):
            self.create_test_files({"TEC_test_file.tec": PLUGIN_TEST_FILE})
        elif self.check_test_tag("create_incorrect_file"):
            self.create_test_files({"TEC_test_file.ini": {"test": 1}})

    def tearDown(self):
        self.delete_test_files()
        super().tearDown()

    def send_default_post_and_return_response(self):
        with open(self.test_files_full_path[0], "r", encoding="utf-8") as file:
            data = {
                "plugin_name": ["test 01'5<>(){}[]a'n\"*"],
                "plugin_version": ["0.1"],
                "plugin_language": ["Polish"],
                "plugin_file": file,
            }
            return self.client.post("/the_elder_commands/plugins/", data=data)

    def test_plugins_use_template(self):
        response = self.client.get("/the_elder_commands/plugins/")
        self.assertTemplateUsed(response, "the_elder_commands/plugins.html")

    @tag("create_test_file")
    def test_view_pass_plugins(self):
        self.send_default_post_and_return_response()
        response = self.client.get("/the_elder_commands/plugins/")
        self.assertEqual(
            "test 015an",
            response.context["service"].all_plugins[0].get("name", "")
        )

    @tag("create_test_file")
    def test_view_pass_messages(self):
        response = self.client.get("/the_elder_commands/plugins/")
        self.assertEqual(
            response.context.get("plugins_messages"),
            []
        )
        self.send_default_post_and_return_response()
        response = self.client.get("/the_elder_commands/plugins/")
        self.assertEqual(
            response.context["plugins_messages"],
            [ADD_PLUGIN_SUCCESS_MESSAGE]
        )

    @tag("create_incorrect_file")
    def test_view_show_error_message(self):
        response = self.send_default_post_and_return_response()
        self.client.get("/the_elder_commands/plugins/")
        self.assertEqual(
            response.context["plugins_messages"],
            [ADD_PLUGIN_FILE_ERROR_MESSAGE]
        )

    @tag("create_test_file")
    def test_success_message_dont_show_after_reload(self):
        self.send_default_post_and_return_response()
        self.client.get("/the_elder_commands/plugins/")
        response = self.client.get("/the_elder_commands/plugins/")
        self.assertEqual(
            response.context["plugins_messages"],
            []
        )

    @tag("create_test_file")
    def test_plugins_redirect_after_POST(self):
        response = self.send_default_post_and_return_response()
        self.assertRedirects(response, "/the_elder_commands/plugins/")

        post = {"selected": "test_015an", "test_015an_variant": "0.1;polish", "test_015an_load_order": "01"}
        response = self.client.post("/the_elder_commands/plugins/", data=post)
        self.assertRedirects(response, "/the_elder_commands/plugins/")

    @tag("create_test_file")
    def test_pass_POST_to_model(self):
        self.send_default_post_and_return_response()

        plugin_model = Plugins.objects.first()
        variants_model = PluginVariants.objects.first()

        plugin_cases = {
            "name": "test 015an",
            "usable_name": "test_015an",
            }
        for field, desired_result in plugin_cases.items():
            self.assertEqual(
                plugin_model.__getattribute__(field),
                desired_result
            )

        variants_cases = {
            "version": "0.1",
            "language": "Polish",
            "plugin_data": PLUGIN_TEST_DICT,
        }
        for field, desired_result in variants_cases.items():
            self.assertEqual(
                variants_model.__getattribute__(field),
                desired_result
            )

    @tag("create_test_file")
    @patch("the_elder_commands.views.PluginVariantsForm")
    def test_file_is_changed_to_dict_before_pass_POST_to_form(self, form_mock):
        self.send_default_post_and_return_response()

        expected = QueryDict("", mutable=True)
        plugin = Plugins.objects.first()
        expected.update({
            'version': '0.1', 'language': 'Polish', 'plugin_data': PLUGIN_TEST_DICT
        })
        form_mock.assert_called_once()
        form_mock.assert_called_with(data=expected, instance=plugin)

    @patch("the_elder_commands.views.SelectedPluginsForm")
    def test_select_post_is_managed_by_correct_form(self, form_mock):
        post = {"selected": "", "test_01_selected": "", "test_01_variant": "0.1;english", "test_01_load_order": "01"}
        self.client.post("/the_elder_commands/plugins/", data=post)
        expected = QueryDict("", mutable=True)
        expected.update(post)

        form_mock.assert_called_once()
