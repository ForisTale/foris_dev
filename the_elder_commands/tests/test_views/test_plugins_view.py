from django.test import TestCase
from django.test.utils import tag
from django.http import QueryDict
from the_elder_commands.views import extract_dict_from_plugin_file, create_variants_data_post
from the_elder_commands.models import Plugins, PluginVariants
from the_elder_commands.inventory import ADD_PLUGIN_SUCCESS_MESSAGE, \
    PLUGIN_TEST_FILE, PLUGIN_TEST_DICT, ADD_PLUGIN_FILE_ERROR_MESSAGE
from the_elder_commands.utils import ManageTestFiles
from unittest.mock import patch
from io import StringIO, BytesIO
import copy


class PluginsTest(TestCase):
    def test_plugins_use_template(self):
        response = self.client.get("/the_elder_commands/plugins/")
        self.assertTemplateUsed(response, "the_elder_commands/plugins.html")

    def test_redirect_after_unselect_post(self):
        post = {"unselect": ["test_01"]}
        response = self.client.post("/the_elder_commands/plugins/", data=post)
        self.assertRedirects(response, "/the_elder_commands/plugins/")


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
        with open(self.test_file_full_path, "r", encoding="utf-8") as file:
            data = {
                "plugin_name": ["test 01'5<>(){}[]a'n\"*"],
                "plugin_version": ["0.1"],
                "plugin_language": ["Polish"],
                "plugin_file": file,
                "add_plugin": ""
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
            response.context["service"].all_plugins[0].name
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
        self.send_default_post_and_return_response()
        response = self.client.get("/the_elder_commands/plugins/")
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
        correct_dict = copy.deepcopy(PLUGIN_TEST_DICT)
        correct_dict.pop("isEsl")
        variants_cases = {
            "version": "0.1",
            "language": "Polish",
            "plugin_data": correct_dict,
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
        correct_dict = copy.deepcopy(PLUGIN_TEST_DICT)
        correct_dict.pop("isEsl")
        expected.update({
            'version': '0.1', 'language': 'Polish', 'plugin_data': correct_dict, "is_esl": False
        })
        form_mock.assert_called_once()
        form_mock.assert_called_with(data=expected, instance=plugin)


class ExtractDictFromPluginFilePost(TestCase):

    def test_can_process_file_into_dict(self):
        with StringIO(PLUGIN_TEST_FILE) as file:
            class FakeRequest:
                FILES = {"plugin_file": file}

            actual = extract_dict_from_plugin_file(FakeRequest)

            self.maxDiff = None
            self.assertDictEqual(actual, PLUGIN_TEST_DICT)

    def test_catch_json_decode_error(self):
        with StringIO(" ") as file:
            class FakeRequest:
                FILES = {"plugin_file": file}

            request = FakeRequest()
            extract_dict_from_plugin_file(request)  # Should not raises!
        self.assertTrue(True)

    def test_catch_json_attribute_error(self):
        class FakeRequest:
            FILES = {"plugin_file": 1}

        request = FakeRequest()
        extract_dict_from_plugin_file(request)  # Should not raises!
        self.assertTrue(True)

    def test_catch_unicode_error(self):
        with BytesIO(b"\x81") as file:
            class FakeRequest:
                FILES = {"plugin_file": file}

            request = FakeRequest()
            extract_dict_from_plugin_file(request)  # Should not raises!
        self.assertTrue(True)


class CreateVariantsDataPost(TestCase):

    def test_pass_all_data_correctly(self):
        with StringIO(PLUGIN_TEST_FILE) as file:
            class FakeRequest:
                FILES = {"plugin_file": file}
                POST = {"plugin_version": 1, "plugin_language": 2}
            expected_dict = copy.deepcopy(PLUGIN_TEST_DICT)
            expected_dict.pop("isEsl")

            request = FakeRequest()
            post = create_variants_data_post(request)
            self.assertEqual(post.get("version"), 1)
            self.assertEqual(post.get("language"), 2)
            self.assertEqual(post.get("is_esl"), False)
            self.assertDictEqual(post.get("plugin_data"), expected_dict)

    def test_pop_is_esl_from_extracted_dict(self):
        with StringIO(PLUGIN_TEST_FILE) as file:
            class FakeRequest:
                FILES = {"plugin_file": file}
                POST = {}
            expected = copy.deepcopy(PLUGIN_TEST_DICT)
            expected.pop("isEsl")

            request = FakeRequest()
            post = create_variants_data_post(request)
            self.assertDictEqual(post.get("plugin_data"), expected)

    def test_missing_is_esl_key_make_function_return_none(self):
        with StringIO('{\"test\": []}') as file:
            class FakeRequest:
                FILES = {"plugin_file": file}
                POST = {}
            self.assertEqual(create_variants_data_post(FakeRequest()), None)

    def test_catch_attribute_error_from_incorrect_file(self):
        with StringIO(" ") as file:
            class FakeRequest:
                FILES = {"plugin_file": file}
                POST = {}
            post = create_variants_data_post(FakeRequest())  # Should not raises
            self.assertEqual(post, None)


class SelectedPluginsTest(TestCase):

    def test_redirect_after_post(self):
        Plugins.objects.create(name="test 01", usable_name="test_01")

        post = {"selected": "test_01", "test_01_variant": "0.1&polish&", "test_01_load_order": "01"}
        response = self.client.post("/the_elder_commands/plugins/", data=post)
        self.assertRedirects(response, "/the_elder_commands/plugins/")

    @patch("the_elder_commands.views.SelectedPluginsForm")
    def test_select_post_is_managed_by_correct_form(self, form_mock):
        post = {"selected": "", "test_01_selected": "", "test_01_variant": "0.1&english&", "test_01_load_order": "01"}
        self.client.post("/the_elder_commands/plugins/", data=post)
        expected = QueryDict("", mutable=True)
        expected.update(post)

        form_mock.assert_called_once()
