from functional_tests import base


class FunctionalTest(base.FunctionalTest):

    def setUp(self):
        super().setUp()
        self.live_server_url = self.live_server_url + "/the_elder_commands"

    def equal_find_element_by_id(self, id_text, value):
        self.wait_for(lambda: self.assertEqual(
                self.driver.find_element_by_id(id_text).text,
                value
            )
        )
