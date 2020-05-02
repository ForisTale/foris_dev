from functional_tests import base


class FunctionalTest(base.FunctionalTest):

    def setUp(self):
        super().setUp()
        self.live_server_url = self.live_server_url + "/the_elder_commands"
