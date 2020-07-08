from functional_tests.the_elder_commands.tec_base import FunctionalTest
from django.test.utils import tag
from the_elder_commands.utils_for_tests import check_test_tag, populate_plugins_table, click_javascript_button
from the_elder_commands.inventory import NO_PLUGIN_SELECTED_ERROR_MESSAGE, COMMANDS_SUCCESS_MESSAGE


class OtherTest(FunctionalTest):

    def setUp(self):
        super().setUp()
        populate_plugins_table()
        if check_test_tag(self, "dont_select"):
            pass
        else:
            self.select_plugin()

        self.driver.get(self.live_server_url + "/other/")

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

    def test_select_some_values_and_show_commands_on_commands_page(self):
        # Foris select all variety and location
        variety = self.wait_for(lambda: self.driver.find_element_by_id("id_variety_tbody"))
        [value.send_keys("10") for value in variety.find_elements_by_tag_name("input")]
        locations = self.driver.find_element_by_id("id_locations_table")
        locations_inputs = locations.find_elements_by_tag_name("input")
        locations_inputs[1].click()

        # locations are links
        locations_links = locations.find_elements_by_tag_name("a")
        self.assertEqual(locations_links[1].get_attribute('href'),
                         "https://elderscrolls.fandom.com/wiki/Whiterun_(Skyrim)")

        # change to words of power and select one
        self.driver.find_element_by_link_text("Words Of Power").click()
        wop_table = self.wait_for(lambda: self.driver.find_element_by_id("id_wordsofpower_table"))
        self.wait_for(lambda: wop_table.find_element_by_tag_name("input").click())

        # then change to perks and select one
        self.driver.find_element_by_link_text("Perks").click()
        perks_table = self.wait_for(lambda: self.driver.find_element_by_id("id_perks_table"))
        self.wait_for(lambda: perks_table.find_element_by_tag_name("input").click())

        # after that he press button, message appear
        click_javascript_button(self, "submit_table")
        wrappers = self.wait_for(lambda: self.driver.find_elements_by_class_name("alert-primary"))
        [self.assertEqual(wrapper.text, COMMANDS_SUCCESS_MESSAGE + "\n×")
         for wrapper in wrappers if wrapper.is_displayed()]

        # then he move to commands page where he sees all commands
        self.driver.find_element_by_link_text("Commands").click()
        commands_list = self.wait_for(lambda: self.driver.find_element_by_id("id_commands_list").text)
        expected = "Commands List:\nplayer.additem 0000000F 10\nplayer.modav dragonsouls 10\nplayer.modav health 10\n" \
                   "player.modav magicka 10\nplayer.modav stamina 10\nplayer.modav carryweight 10\nplayer.setav " \
                   "speedmult 10\nplayer.teachword 010602A5\nplayer.addperk 0101711C\ncoc Whiterun"
        self.assertEqual(commands_list, expected)

    def test_reset_tables(self):
        # Foris add some gold, then generate commands
        self.wait_for(lambda: self.driver.find_element_by_name("gold").send_keys("1000"))
        click_javascript_button(self, "submit_table")

        # but he change mind and reset table.
        click_javascript_button(self, "reset_tables")
        self.wait_for(lambda: self.assertEqual(self.driver.find_element_by_name("gold").get_attribute("value"), ""))
