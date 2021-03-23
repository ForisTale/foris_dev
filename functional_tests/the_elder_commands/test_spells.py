from functional_tests.the_elder_commands.tec_base import FunctionalTest
from django.test.utils import tag
from the_elder_commands.utils_for_tests.populate_plugins_table import populate_plugins_table
from the_elder_commands.utils_for_tests.check_test_tag import check_test_tag
from the_elder_commands.utils_for_tests.click_javascript_button import click_javascript_button
from the_elder_commands.inventory import NO_PLUGIN_SELECTED_ERROR_MESSAGE, COMMANDS_SUCCESS_MESSAGE


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
        self.driver.find_element_by_class_name("submit_table").click()

    @tag("dont_select")
    def test_need_selected_plugin(self):
        # Foris forgot to select plugin so he was redirected to plugin page
        self.wait_for(lambda: self.assertEqual(self.driver.current_url, self.live_server_url + "/plugins/"))
        error_message = self.driver.find_element_by_class_name("alert").text
        self.assertIn(NO_PLUGIN_SELECTED_ERROR_MESSAGE, error_message)

    def test_selected_spells_show_in_commands_page(self):
        # Foris sees spell categories and WoP category
        categories = self.wait_for(lambda: self.driver.find_element_by_id("id_spells_categories"))
        expected = "Alteration\nConjuration\nDestruction\nIllusion\nRestoration\nOther"
        self.assertEqual(expected, categories.text)
        # alteration is selected
        self.assertEqual(categories.find_element_by_class_name("active").text, "Alteration")
        # each category have table with correct headers
        tables = self.driver.find_elements_by_tag_name("table")
        nav_tabs = self.driver.find_element_by_class_name("nav-tabs")
        category_links = nav_tabs.find_elements_by_tag_name("a")
        inputs = self.driver.find_elements_by_tag_name("input")
        for index, table in enumerate(tables):
            category_links[index].click()
            header = self.wait_for(lambda: table.find_elements_by_tag_name("th"))
            actual = {th.text for th in header}
            expected = {"Selected", "Spell name", "Form ID", "Editor ID", "Mastery", "Effects", "Plugin"}
            self.assertEqual(expected, actual, msg=f"Fail on {table.get_attribute('id')}")
            self.wait_for(lambda: table.find_element_by_tag_name("input"))
            [checkbox.click() for checkbox in inputs if checkbox.is_displayed()]

            # then he press generate commands
            click_javascript_button(self, "submit_table")

            # after press he sees message
            wrappers = self.wait_for(lambda: self.driver.find_elements_by_class_name("alert-primary"))
            for wrapper in wrappers:
                if wrapper.is_displayed():
                    self.assertEqual(wrapper.text, COMMANDS_SUCCESS_MESSAGE + "\n×")

        # now Foris go to commands page
        self.driver.find_element_by_link_text("Commands").click()
        # and there he sees all spells commands
        commands_list = self.wait_for(lambda: self.driver.find_element_by_id("id_commands_list").text)
        expected = "Commands List:\nplayer.addspell 01000001\nplayer.addspell 01000002\nplayer.addspell 0110FD5F\n" \
                   "player.addspell 01000003\nplayer.addspell 01000004\nplayer.addspell 01000005"
        self.assertEqual(commands_list, expected)

    def test_reset_button(self):
        # Foris add some gold, then generate commands
        self.wait_for(lambda: self.driver.find_element_by_tag_name("input").click())
        click_javascript_button(self, "submit_table")

        # but he change mind and reset table.
        click_javascript_button(self, "reset_tables")
        self.wait_for(lambda: self.assertEqual(self.driver.find_element_by_tag_name("input").get_attribute("value"),
                                               ""))
