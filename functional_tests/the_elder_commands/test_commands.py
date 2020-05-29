from .tec_base import FunctionalTest


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
