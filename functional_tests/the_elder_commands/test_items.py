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

    def test_default_looks(self):
        # And in title Foris sees website name.
        self.assertEqual(self.driver.title, "The Elder Commands")

        # Then he sees bar with categories,
        links = [link.text for link in self.driver.find_elements_by_tag_name("a")]
        categories = ["Character", "Items", "Spells", "Other", "Plugins"]
        for category in categories:
            self.assertIn(
                category,
                links
            )

        # he chose "Items".
        base_url = self.driver.current_url
        self.driver.find_element_by_link_text("Items").click()

        # and move to items category
        self.wait_for(lambda: self.assertEqual(
            self.driver.current_url,
            base_url + "items/"
        ))

        # After page load Foris spot that "items" is active,
        self.assertIn(
            "Items",
            self.driver.find_element_by_class_name("active").text
        )

        # there is table to chose plugin.

        # Foris select one of the plugins and press select,

        # and after selecting, table hide under button.

        # Now Foris sees items category he can chose from.

        # Weapons is selected, Foris change to armors.

        self.fail("Finish test!")
