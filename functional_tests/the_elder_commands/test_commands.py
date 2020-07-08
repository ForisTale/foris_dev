from .tec_base import FunctionalTest
from the_elder_commands.utils_for_tests import populate_plugins_table, click_javascript_button


class CommandsTest(FunctionalTest):

    def setUp(self):
        super().setUp()
        self.base_url = self.live_server_url + "/commands/"
        self.download_url = self.live_server_url + "/commands/download"

        self.driver.get(self.live_server_url)
        self.driver.find_element_by_name("onehanded_new").send_keys("50")
        self.driver.find_element_by_id("id_calculate").click()
        self.driver.find_element_by_link_text("Commands").click()

    def test_can_download_file(self):
        self.driver.get(self.base_url)
        link = self.driver.find_element_by_class_name("download")
        self.assertEqual(link.get_attribute("href"), self.download_url)

    def test_reset_button(self):
        populate_plugins_table()
        self.driver.get(self.live_server_url + "/plugins/")
        self.wait_for(lambda: self.driver.find_element_by_class_name("test_01").click())
        self.driver.find_element_by_name("test_01_load_order").send_keys("01")
        self.driver.find_element_by_id("id_select_plugin_submit").click()

        # Foris generate skills
        self.driver.get(self.live_server_url + "/skills/")
        self.driver.find_element_by_id("id_calculate").click()
        # items
        self.driver.get(self.live_server_url + "/items/")
        table_body = self.wait_for(lambda: self.driver.find_element_by_id("id_weapons_tbody"))
        self.wait_for(lambda: table_body.find_element_by_tag_name("input").send_keys("80"))
        click_javascript_button(self, "submit_table")
        self.wait_for(lambda: self.driver.find_element_by_class_name("alert-primary"))
        # spells
        self.driver.get(self.live_server_url + "/spells/")
        table_body = self.wait_for(lambda: self.driver.find_element_by_id("id_alteration_table"))
        self.wait_for(lambda: table_body.find_element_by_tag_name("input").click())
        click_javascript_button(self, "submit_table")
        self.wait_for(lambda: self.driver.find_element_by_class_name("alert-primary"))
        # gold
        self.driver.get(self.live_server_url + "/other/")
        table_body = self.wait_for(lambda: self.driver.find_element_by_id("id_variety_table"))
        self.wait_for(lambda: table_body.find_element_by_name("gold").send_keys("80"))
        click_javascript_button(self, "submit_table")
        self.wait_for(lambda: self.driver.find_element_by_class_name("alert-primary"))
        # then he check commands
        self.driver.get(self.base_url)
        self.wait_for(lambda:
                      self.assertEqual(
                          self.driver.find_element_by_id("id_commands_list").text,
                          "Commands List:\nplayer.advskill onehanded 10051\nplayer.additem 01017009 80\n"
                          "player.addspell 01000001\nplayer.additem 0000000F 80"))

        # but he change mind and reset all.
        self.driver.find_element_by_class_name("reset").click()
        self.wait_for(lambda: self.assertEqual(self.driver.find_element_by_id("id_commands_list").text,
                                               "Commands List:"))
