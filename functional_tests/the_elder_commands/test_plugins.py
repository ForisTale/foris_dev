from functional_tests.the_elder_commands.tec_base import FunctionalTest
from the_elder_commands.models import Plugins, PluginVariants
from selenium.webdriver.support.ui import Select
from the_elder_commands.inventory import PLUGIN_TEST_FILE, ManageTestFiles, ADD_PLUGIN_SUCCESS_MESSAGE, \
    ADD_PLUGIN_FILE_ERROR_MESSAGE, ADD_PLUGIN_PLUGIN_EXIST_ERROR_MESSAGE, PLUGIN_TEST_DICT
from django.test.utils import tag
import copy


class PluginsTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        # Foris open plugins section of TEC
        self.driver.get(self.live_server_url + "/plugins/")

    def check_is_active(self, id_string):
        active_elements_id = [element.id for element in self.driver.find_elements_by_class_name("active")]
        self.assertIn(
            self.driver.find_element_by_id(id_string).id,
            active_elements_id
        )

    def test_default_looks(self):
        # He sees row with with links
        self.wait_for(lambda: self.assertEqual(
            "Plugins\nAdd Plugin",
            self.driver.find_element_by_class_name("nav-tabs").text
        ))

        # "plugins" is active.
        self.check_is_active("id_plugins")

        # he click on add plugin
        self.driver.find_element_by_link_text("Add Plugin").click()
        self.check_is_active("id_add_plugin")

        # there he sees form
        form_text = self.driver.find_element_by_id("id_add_plugin_form").text
        cases = ["Plugin name", "Select a language", "Mod version", "Select .tec file", "Submit"]
        for case in cases:
            self.assertIn(
                case,
                form_text
            )

        # he change back to plugins
        self.driver.find_element_by_id("id_plugins").click()
        self.check_is_active("id_plugins")

        # and there is table
        self.assertEqual(
            self.driver.find_element_by_id("id_plugins_table").text,
            "Plugin Name Version and Language Plugin Order Selected?"
        )
        self.assertEqual(
            self.driver.find_element_by_id("id_selected_plugins_table").text,
            "Selected Plugins:\nUnselect All"
        )


class AddPluginTest(FunctionalTest, ManageTestFiles):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ManageTestFiles.__init__(self)

    def setUp(self):
        super().setUp()

        if self.check_test_tag("create_test_file"):
            data = {"TEC_plugin_test_file.tec": PLUGIN_TEST_FILE}
            self.create_test_files(data)
        if self.check_test_tag("create_incorrect_file"):
            incorrect_data = {"TEC_incorrect_file.ini": b'3432342343'}
            self.create_test_files(incorrect_data)
        if self.check_test_tag("populate_plugins_table"):
            self.populate_plugins_table()

        # Foris open plugins section of TEC,
        self.driver.get(self.live_server_url + "/plugins/")

    def tearDown(self):
        self.delete_test_files()
        super().tearDown()

    def submit_add_file(self, name, version, language, file_full_path):
        # then chose add plugin
        self.wait_for(lambda: self.driver.find_element_by_link_text("Add Plugin").click())

        self.driver.find_element_by_id("id_plugin_name").send_keys(name)
        self.driver.find_element_by_id("id_plugin_version").send_keys(version)

        select = Select(self.driver.find_element_by_id("id_plugin_language"))
        select.select_by_visible_text(language)

        upload_window = self.driver.find_element_by_id("id_plugin_file")
        upload_window.send_keys(file_full_path)

        self.driver.find_element_by_id("id_add_plugin_submit").click()

    @staticmethod
    def populate_plugins_table():
        for index in range(4):
            plugin = Plugins.objects.create(name="test 0" + str(index+1), usable_name="test_0" + str(index+1))
            plugin.save()
            for num in range(4):
                form = PluginVariants.objects.create(
                    instance=plugin,
                    version="0" + str(num+1),
                    language="english",
                    plugin_data=copy.deepcopy(PLUGIN_TEST_DICT)
                )
                form.save()

    def check_errors_messages(self, list_of_messages):
        errors_messages = self.wait_for(lambda: self.driver.find_elements_by_class_name("errors_messages"))
        errors_messages = [error.text for error in errors_messages]
        for index in range(len(errors_messages)):
            try:
                self.assertEqual(errors_messages[index], list_of_messages[index] + "\n×")
            except IndexError:
                self.fail(f"There is more or less errors than expected! Errors:\n{errors_messages}")

    @tag("create_test_file")
    def test_add_plugin_to_database_and_show_in_plugins_table(self):
        # He fill form to add plugin and submit it
        self.submit_add_file("test mod", "0.1", "Polish", self.test_files_full_path[0])

        # in table he sees plugin that he add
        self.assertEqual(
            "test mod\n0.1 Polish",
            self.driver.find_element_by_class_name("plugins_table").text
        )

        # with "Selected?" unchecked and empty "Plugin Order"
        self.assertFalse(self.driver.find_element_by_class_name("test_mod").is_selected())
        self.assertEqual(self.driver.find_element_by_name("test_mod_load_order").get_attribute("value"), "")

        # after that he sees message with information of successfully added plugin
        self.check_errors_messages([ADD_PLUGIN_SUCCESS_MESSAGE])

    @tag("create_incorrect_file")
    def test_add_plugin_give_error_message_when_file_is_incorrect(self):
        # He fill form and submit it
        self.submit_add_file("test mod", "0.1", "English", self.test_files_full_path[0])

        # but he get message that file was incorrect
        self.check_errors_messages([ADD_PLUGIN_FILE_ERROR_MESSAGE])

    @tag("create_test_file")
    def test_files_with_same_data_return_error(self):
        # Foris by mistake send two the same files.
        self.submit_add_file("test mod", "0.1", "Polish", self.test_files_full_path[0])
        self.submit_add_file("test mod", "0.1", "Polish", self.test_files_full_path[0])

        # and he sees error.
        self.check_errors_messages([ADD_PLUGIN_PLUGIN_EXIST_ERROR_MESSAGE])

    @tag("create_test_file")
    def test_plugins_with_same_name_show_options_to_chose_variants(self):
        # Foris submit few mods with different language and version
        self.submit_add_file("test mod", "0.1", "Polish", self.test_files_full_path[0])
        self.submit_add_file("test mod", "0.1", "English", self.test_files_full_path[0])
        self.submit_add_file("test mod", "0.2", "Polish", self.test_files_full_path[0])
        self.submit_add_file("test mod", "0.2", "English", self.test_files_full_path[0])

        # then he can chose between variants
        self.wait_for(lambda: self.assertEqual(
            "test mod\n0.2 English\n0.2 Polish\n0.1 English\n0.1 Polish",
            self.driver.find_element_by_class_name("plugins_table").text
        ))

        plugins_table = self.driver.find_element_by_class_name("plugins_table")
        table_rows = plugins_table.find_elements_by_tag_name("tr")
        self.assertEqual(
            len(table_rows),
            1
        )

        self.driver.find_element_by_id("id_test_mod_variant").click()
        options = self.driver.find_elements_by_name("test_mod_variant")
        options = [option.text for option in options]
        expected = ['0.2 English\n0.2 Polish\n0.1 English\n0.1 Polish']
        self.assertEqual(options, expected)

    @tag("populate_plugins_table")
    def test_can_chose_plugins_to_select_and_selected_plugins_are_show_in_table(self):
        # Foris chose few plugins and fill their load order
        self.wait_for(lambda: self.driver.find_element_by_class_name("test_01").click())
        self.driver.find_element_by_name("test_01_load_order").send_keys("01")
        self.driver.find_element_by_class_name("test_02").click()
        self.driver.find_element_by_name("test_02_load_order").send_keys("02")

        # then he submit them
        self.driver.find_element_by_id("id_select_plugin_submit").click()

        # and after reload selected plugins appear in table on the side
        self.wait_for(lambda: self.assertEqual(
            self.driver.find_element_by_class_name("selected_plugins").text,
            "test 01 ver: 04 English\nUnselect\ntest 02 ver: 04 English\nUnselect"
        ))

        # he decide thant he don't need one of them
        selected_table = self.wait_for(lambda: self.driver.find_element_by_class_name("selected_plugins"))
        selected_table.find_element_by_name("unselect").click()

        self.wait_for(lambda: self.assertEqual(
            self.driver.find_element_by_class_name("selected_plugins").text,
            "test 02 ver: 04 English\nUnselect"
        ))

        # then he add one more plugin
        self.wait_for(lambda: self.driver.find_element_by_class_name("test_03").click())
        self.driver.find_element_by_name("test_03_load_order").send_keys("03")
        self.driver.find_element_by_id("id_select_plugin_submit").click()

        self.wait_for(lambda: self.assertEqual(
            self.driver.find_element_by_class_name("selected_plugins").text,
            "test 02 ver: 04 English\nUnselect\ntest 03 ver: 04 English\nUnselect"
        ))

        # but decided that he don't need any of them and unselect all
        self.wait_for(lambda: self.driver.find_element_by_class_name("unselect_all").click())

        self.wait_for(lambda: self.assertEqual(
            self.driver.find_element_by_class_name("selected_plugins").text,
            ""
        ))
