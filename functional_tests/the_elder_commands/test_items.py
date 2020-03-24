from functional_tests.the_elder_commands.tec_base import FunctionalTest


class ItemsTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        # TODO make testing database.

        # Foris open The elder commands website.
        self.driver.get(self.live_server_url)

    def tearDown(self):
        super().tearDown()
        # TODO clean database.

    def test_default_look(self):
        # there is table to chose plugin.

        # Foris select one of the plugins and press select,

        # and after selecting, table hide under button.

        # Now Foris sees items category he can chose from.

        # Weapons is selected, Foris change to armors.

        self.fail("Finish test!")
