from .superlist_base import FunctionalTest

import time


class SuperlistLayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith going to the home page
        self.driver.get(self.live_server_url)
        self.driver.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        input_box = self.get_item_input_box()
        time.sleep(2)
        self.assertAlmostEqual(
            input_box.location["x"] + input_box.size["width"] / 2,
            512,
            delta=10
        )

        # She start a new list and sees the input is nicely centered there too
        self.add_list_item("testing")
        input_box = self.get_item_input_box()
        self.assertAlmostEqual(
            input_box.location["x"] + input_box.size["width"] / 2,
            512,
            delta=10
        )
