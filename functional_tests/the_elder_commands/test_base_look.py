from .tec_base import FunctionalTest


class DefaultLookTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.driver.get(self.live_server_url)

    def test_base_looks(self):
        # And in title Foris sees website name.
        self.assertEqual(self.driver.title, "The Elder Commands")

        # Then he sees bar with categories,
        links = [link.text for link in self.driver.find_elements_by_class_name("header-link")]
        categories = ["Foris.dev", "Skills", "Items", "Spells", "Other", "Plugins", "Commands"]
        self.assertListEqual(links, categories)
