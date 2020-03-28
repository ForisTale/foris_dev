from functional_tests.the_elder_commands.tec_base import FunctionalTest


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
            self.driver.find_element_by_id("id_plugin_table").text,
            "Selected? Plugin Name Language and version Plugin Order"
        )
        self.assertEqual(
            self.driver.find_element_by_id("id_selected_plugins_table").text,
            "Selected Plugins:"
        )
