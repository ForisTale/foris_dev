from functional_tests.the_elder_commands.tec_base import FunctionalTest
from selenium.webdriver.support.ui import Select
from the_elder_commands.inventory import PLUGIN_TEST_FILE, ManageTestFiles
from django.test.utils import tag


class PluginsTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        # Foris open plugins section of TEC
        self.driver.get(self.live_server_url + "/plugins/")

    def check_id_is_active(self, id_string):
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
        self.check_id_is_active("id_plugins")

        # he click on add plugin
        self.driver.find_element_by_link_text("Add Plugin").click()
        self.check_id_is_active("id_add_plugin")

        # there he sees form
        form_text = self.driver.find_element_by_tag_name("form").text
        cases = ["Plugin name", "Select a language", "Mod version", "Select .tec file", "Submit"]
        for case in cases:
            self.assertIn(
                case,
                form_text
            )

        # he change back to plugins
        self.driver.find_element_by_id("id_plugins").click()
        self.check_id_is_active("id_plugins")

        # and there is table
        self.assertEqual(
            self.driver.find_element_by_id("id_plugins_table").text,
            "Selected? Plugin Name Language and version Plugin Order"
        )
        self.assertEqual(
            self.driver.find_element_by_id("id_selected_plugins_table").text,
            "Selected Plugins:"
        )


class AddPluginTest(FunctionalTest, ManageTestFiles):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ManageTestFiles.__init__(self)

    def setUp(self):
        super().setUp()
        data = {"TEC_plugin_test_file.tec": PLUGIN_TEST_FILE}
        if self.check_test_tag("create_test_file"):
            self.create_test_files(data)

        # Foris open plugins section of TEC,
        self.driver.get(self.live_server_url + "/plugins/")
        # then chose add plugin
        self.driver.find_element_by_link_text("Add Plugin").click()

    def tearDown(self):
        self.delete_test_files()
        super().tearDown()

    @tag("create_test_file")
    def test_add_plugin_to_database_and_show_in_plugins_table(self):
        # He fill form to add plugin and submit it
        self.driver.find_element_by_id("id_plugin_name").send_keys("test mod")
        self.driver.find_element_by_id("id_plugin_version").send_keys("0.1")

        select = Select(self.driver.find_element_by_id("id_plugin_language"))
        select.select_by_visible_text("Polish")

        upload_window = self.driver.find_element_by_id("id_plugin_file")
        upload_window.send_keys(self.test_files_full_path[0])

        self.driver.find_element_by_id("id_plugin_submit").click()

        # in table he sees plugin that he add
        self.assertEqual(
            "test mod 0.1 Polish",
            self.driver.find_element_by_class_name("plugins_table").text
        )

        # with "Selected?" unchecked and empty "Plugin Order"
        self.assertEqual(
            self.driver.find_element_by_name("test_mod_selected").get_attribute("value"),
            "on"
        )
        self.assertEqual(
            self.driver.find_element_by_name("test_mod_plugin_order").get_attribute("value"),
            ""
        )

        # after that he sees message with information of successfully added plugin
        self.wait_for(lambda: self.assertIn(
            "Plugin was successfully added to database.",
            self.driver.find_element_by_tag_name("body").text
        ))

    def test_add_plugin_give_error_message_when_file_is_incorrect(self):
        self.fail("Finish Test!")
