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
        links = [link.text for link in self.driver.find_elements_by_class_name("header-link")]
        categories = ["Foris.dev", "Character", "Items", "Spells", "Other", "Plugins", "Commands"]
        self.assertListEqual(links, categories)

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

        # Foris sees items category he can chose from.

        # Weapons is selected, Foris change to armors.

        self.fail("Finish test!")

    def test_not_selected_plugins_redirect_to_plugins_page_with_message(self):
        self.fail("Finish test!")
