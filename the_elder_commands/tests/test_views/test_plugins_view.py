from django.test import TestCase
from django.test.utils import tag
from django.http import QueryDict
from the_elder_commands.views import unselect
from the_elder_commands.models import Plugins, PluginVariants
from the_elder_commands.inventory import ManageTestFiles, ADD_PLUGIN_SUCCESS_MESSAGE, \
    PLUGIN_TEST_FILE, PLUGIN_TEST_DICT, ADD_PLUGIN_FILE_ERROR_MESSAGE
from unittest.mock import patch


class PluginsTest(TestCase):
    def test_plugins_use_template(self):
        response = self.client.get("/the_elder_commands/plugins/")
        self.assertTemplateUsed(response, "the_elder_commands/plugins.html")


class AddPluginTest(TestCase, ManageTestFiles):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ManageTestFiles.__init__(self)

    def setUp(self):
        super().setUp()
        self.maxDiff = None

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

    @tag("create_test_file")
    def test_redirect_after_POST(self):
        response = self.send_default_post_and_return_response()
        self.assertRedirects(response, "/the_elder_commands/plugins/")

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


class SelectedPluginsTest(TestCase):

    def test_redirect_after_post(self):
        Plugins.objects.create(name="test 01", usable_name="test_01")

        post = {"selected": "test_01", "test_01_variant": "0.1;polish", "test_01_load_order": "01"}
        response = self.client.post("/the_elder_commands/plugins/", data=post)
        self.assertRedirects(response, "/the_elder_commands/plugins/")

    @patch("the_elder_commands.views.SelectedPluginsForm")
    def test_select_post_is_managed_by_correct_form(self, form_mock):
        post = {"selected": "", "test_01_selected": "", "test_01_variant": "0.1;english", "test_01_load_order": "01"}
        self.client.post("/the_elder_commands/plugins/", data=post)
        expected = QueryDict("", mutable=True)
        expected.update(post)

        form_mock.assert_called_once()


class UnselectPluginTest(TestCase):

    def test_redirect_after_post(self):
        post = {"unselect": ["test_01"]}
        response = self.client.post("/the_elder_commands/plugins/", data=post)
        self.assertRedirects(response, "/the_elder_commands/plugins/")

    def test_unselect_chosen(self):
        data = QueryDict("", mutable=True)
        data["unselect"] = "test_02"

        class FakeRequest:
            def __init__(self):
                self.POST = data
                self.session = {"selected": [{"usable_name": "test_01"}, {"usable_name": "test_02"},
                                             {"usable_name": "test_03"}]}

        request = FakeRequest()
        unselect(request)
        self.assertEqual(request.session.get("selected"), [{"usable_name": "test_01"}, {"usable_name": "test_03"}])

    def test_unselect_all(self):
        data = QueryDict("", mutable=True)
        data["unselect"] = "unselect_all"

        class FakeRequest:
            def __init__(self):
                self.POST = data
                self.session = {"selected": [{"usable_name": "test_01"}, {"usable_name": "test_02"}]}

        request = FakeRequest()
        unselect(request)
        self.assertEqual(request.session.get("selected"), [])
