from django.test import TestCase
from django.test.utils import tag
from the_elder_commands.models import Plugins, PluginVariants
from the_elder_commands.inventory import ADD_PLUGIN_SUCCESS_MESSAGE, ADD_PLUGIN_ERROR_PLUGIN_EXIST, \
    PLUGIN_TEST_FILE, ADD_PLUGIN_ERROR_FILE, PLUGIN_TEST_EMPTY_DATA, \
    PLUGIN_TEST_DICT_ALTERED_BY_FORM, INCORRECT_LOAD_ORDER
from the_elder_commands.utils import ManageTestFiles
import copy


class PluginsTest(TestCase):
    base_url = "/the_elder_commands/plugins/"

    def test_plugins_use_template(self):
        response = self.client.get(self.base_url)
        self.assertTemplateUsed(response, "the_elder_commands/plugins.html")

    def test_redirect_after_unselect_post(self):
        post = {"unselect": ["test_01"]}
        response = self.client.post(self.base_url, data=post)
        self.assertRedirects(response, self.base_url)


class AddPluginTest(TestCase, ManageTestFiles):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ManageTestFiles.__init__(self)

    def setUp(self):
        super().setUp()
        self.maxDiff = None
        self.base_url = "/the_elder_commands/plugins/"

        if self.check_test_tag("create_test_file"):
            self.create_test_files({"TEC_test_file.tec": PLUGIN_TEST_FILE})
        elif self.check_test_tag("create_incorrect_file"):
            self.create_test_files({"TEC_test_file.ini": {"test": 1}})
        elif self.check_test_tag("create_empty_data"):
            self.create_test_files({"TEC_empty_data.tec": PLUGIN_TEST_EMPTY_DATA})

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
            return self.client.post(self.base_url, data=data)

    @tag("create_test_file")
    def test_redirect_after_POST(self):
        response = self.send_default_post_and_return_response()
        self.assertRedirects(response, self.base_url)

    @tag("create_test_file")
    def test_view_pass_plugins(self):
        self.send_default_post_and_return_response()
        response = self.client.get(self.base_url)
        self.assertEqual(
            "test 015an",
            response.context["service"].all_plugins[0].name
        )

    @tag("create_test_file")
    def test_view_pass_messages(self):
        response = self.client.get(self.base_url)
        self.assertEqual(
            response.context.get("plugins_messages"),
            []
        )
        self.send_default_post_and_return_response()
        response = self.client.get(self.base_url)
        self.assertEqual(
            response.context["plugins_messages"],
            [ADD_PLUGIN_SUCCESS_MESSAGE]
        )

    @tag("create_incorrect_file")
    def test_view_show_error_message(self):
        self.send_default_post_and_return_response()
        response = self.client.get(self.base_url)
        self.assertEqual(
            response.context["plugins_messages"],
            [ADD_PLUGIN_ERROR_FILE]
        )

    @tag("create_test_file")
    def test_add_plugin_give_plugin_exist_error(self):
        self.send_default_post_and_return_response()
        self.send_default_post_and_return_response()
        response = self.client.get(self.base_url)
        self.assertEqual(
            response.context["plugins_messages"][1],
            ADD_PLUGIN_ERROR_PLUGIN_EXIST
        )

    @tag("create_empty_data")
    def test_add_plugin_give_file_error_message(self):
        self.send_default_post_and_return_response()
        response = self.client.get(self.base_url)
        self.assertEqual(
            response.context["plugins_messages"],
            [ADD_PLUGIN_ERROR_FILE]
        )

    @tag("create_test_file")
    def test_success_message_dont_show_after_reload(self):
        self.send_default_post_and_return_response()
        self.client.get(self.base_url)
        response = self.client.get(self.base_url)
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
        correct_dict = copy.deepcopy(PLUGIN_TEST_DICT_ALTERED_BY_FORM)
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


class SelectedPluginsTest(TestCase):
    base_url = "/the_elder_commands/plugins/"

    def test_redirect_after_correct_post(self):
        Plugins.objects.create(name="test 01", usable_name="test_01")
        post = {"selected": "test_01", "test_01_variant": "0.1&polish&", "test_01_load_order": "01"}
        response = self.client.post(self.base_url, data=post)
        self.assertRedirects(response, self.base_url)

    def test_redirect_after_wrong_post(self):
        post = {"selected": "test_01", "test_01_variant": "0.1&english&", "test_01_load_order": "avva"}
        Plugins.objects.create(name="test 01", usable_name="test_01")
        response = self.client.post(self.base_url, data=post)
        self.assertRedirects(response, self.base_url)

    def test_pass_error_message_after_wrong_post(self):
        post = {"selected": "test_01", "test_01_variant": "0.1&english&", "test_01_load_order": "avva"}
        Plugins.objects.create(name="test 01", usable_name="test_01")
        self.client.post(self.base_url, data=post)
        response = self.client.get(self.base_url)
        self.assertEqual(response.context["plugins_messages"], [INCORRECT_LOAD_ORDER])

    def test_data_are_passed_correctly(self):
        Plugins.objects.create(name="test 01", usable_name="test_01")
        post = {"selected": "test_01", "test_01_variant": "0.1&polish&", "test_01_load_order": "01"}
        self.client.post(self.base_url, data=post)
        session = self.client.session
        self.assertEqual(session.get("selected"), [{'esl': '', 'language': 'polish', 'load_order': '01',
                                                    'name': 'test 01', 'usable_name': 'test_01', 'version': '0.1'}])
