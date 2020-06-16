from functional_tests.the_elder_commands.tec_base import FunctionalTest
from django.test.utils import tag
from the_elder_commands.utils_for_tests import check_test_tag, populate_plugins_table
from the_elder_commands.inventory import NO_PLUGIN_SELECTED_ERROR_MESSAGE, template_variables


class SpellsTest(FunctionalTest):

    def setUp(self):
        super().setUp()
        populate_plugins_table()
        if check_test_tag(self, "dont_select"):
            pass
        else:
            self.select_plugin()

        self.driver.get(self.live_server_url + "/spells/")

    def select_plugin(self):
        self.driver.get(self.live_server_url + "/plugins/")
        self.wait_for(lambda: self.driver.find_element_by_class_name("test_01").click())
        self.driver.find_element_by_name("test_01_load_order").send_keys("01")
        self.driver.find_element_by_id("id_select_plugin_submit").click()

    @tag("dont_select")
    def test_need_selected_plugin(self):
        # Foris forgot to select plugin so he was redirected to plugin page
        self.wait_for(lambda: self.assertEqual(self.driver.current_url, self.live_server_url + "/plugins/"))
        error_message = self.driver.find_element_by_class_name("errors_messages").text
        self.assertEqual(error_message, NO_PLUGIN_SELECTED_ERROR_MESSAGE + "\n×")

    def test_default_looks(self):
        # Foris sees spell categories and WoP category
        categories = self.wait_for(lambda: self.driver.find_element_by_id("id_spells_categories"))
        expected = "Alteration\nConjuration\nDestruction\nIllusion\nRestoration\nWords Of Power\nOther"
        self.assertEqual(expected, categories.text)
        # alteration is selected
        self.assertEqual(categories.find_element_by_class_name("active").text, "Alteration")
        # each category have table with correct headers
        tables = self.driver.find_elements_by_tag_name("table")
        nav_tabs = self.driver.find_element_by_class_name("nav-tabs")
        category_links = nav_tabs.find_elements_by_tag_name("a")
        self.assertEqual(len(tables), 7)
        for index, table in enumerate(tables):
            category_links[index].click()
            header = self.wait_for(lambda: table.find_elements_by_tag_name("th"))
            actual = {th.text for th in header}
            if table.get_attribute("id") == "id_wordsofpower_table":
                expected = {"Selected", "Word", "Translation", "Form ID", "Editor ID", "Plugin"}
            else:
                expected = {"Selected", "Spell name", "Form ID", "Editor ID", "Mastery", "Effects", "Plugin"}
            self.assertEqual(expected, actual, msg=f"Fail on {table.get_attribute('id')}")

        # there is button to generate commands
        button = self.driver.find_element_by_class_name("submit_button")
        self.assertEqual(button.text, "Generate\nCommands")
