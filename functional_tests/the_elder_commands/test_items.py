from functional_tests.the_elder_commands.tec_base import FunctionalTest
from the_elder_commands.utils import populate_plugins_table
from django.test.utils import tag
from the_elder_commands.inventory import NO_PLUGIN_SELECTED_ERROR_MESSAGE, template_variables, \
    COMMANDS_SUCCESS_MESSAGE
from the_elder_commands.utils import ManageTestFiles


class ItemsTest(FunctionalTest, ManageTestFiles):
    def setUp(self):
        super().setUp()
        self.maxDiff = None

        if self.check_test_tag("dont_select"):
            pass
        else:
            populate_plugins_table()
            self.select_plugins()

        # Foris open The elder commands website.
        self.driver.get(self.live_server_url + "/items/")

    def check_table_first_data(self, table_id, expected):
        table_body = self.wait_for(lambda: self.driver.find_element_by_id(table_id))
        table_data = table_body.find_elements_by_tag_name("td")
        self.assertEqual(table_data[1].text, expected)

    def select_plugins(self):
        self.driver.get(self.live_server_url + "/plugins/")
        self.wait_for(lambda: self.driver.find_element_by_class_name("test_01").click())
        self.driver.find_element_by_name("test_01_load_order").send_keys("01")
        self.driver.find_element_by_class_name("test_03").click()
        self.driver.find_element_by_name("test_03_load_order").send_keys("03")
        self.driver.find_element_by_id("id_select_plugin_submit").click()

    def submit_items_table(self):
        table = self.driver.find_element_by_class_name("submit_table")
        self.driver.execute_script("arguments[0].click()", table)

    def test_default_looks(self):
        # Foris see default page of TEC but
        self.driver.get(self.live_server_url)

        # he chose to switch to "Items".
        base_url = self.driver.current_url
        self.wait_for(lambda: self.driver.find_element_by_link_text("Items").click())

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
        categories = self.driver.find_element_by_id("id_items_categories")
        expected = "Weapons\nArmors\nAmmo\nBooks\nIngredients\nAlchemy\nScrolls\nSoulGems\nKeys\nMiscellaneous"
        self.assertEqual(categories.text, expected)

        # Weapons is selected, Foris change to armors.
        self.assertEqual(categories.find_element_by_class_name("active").text, "Weapons")

        categories.find_element_by_link_text("Armors").click()

        categories = self.driver.find_element_by_id("id_items_categories")
        self.assertEqual(categories.find_element_by_class_name("active").text, "Armors")

    @tag("dont_select")
    def test_not_selected_plugins_redirect_to_plugins_page_with_message(self):
        # Foris forget to select plugin and when he arrive on items page he get reload to plugins page with
        # error message
        self.wait_for(lambda: self.assertEqual(self.driver.current_url, self.live_server_url+"/plugins/"))
        error_message = self.driver.find_element_by_class_name("errors_messages").text
        self.assertEqual(error_message, NO_PLUGIN_SELECTED_ERROR_MESSAGE + "\n×")

    def test_categories(self):
        # Foris sees weapons table with several items
        self.wait_for(lambda: self.check_table_first_data("id_weapons_tbody", "Daedryczny wielki miecz inferna"))

        # he decide to take one item
        self.driver.find_element_by_tag_name("input").send_keys("1")

        # then he change to each categories and set one item from each.
        various_variables = template_variables(None)
        categories = various_variables.get("items_categories")
        expected = ["", "Buty", "Dwemerski bełt", "Księga czarów: Piorun", "Abecejski długopłetwiak",
                    "Miód", "Spostrzeżenia Shalidora: Magia", "Klejnot duszy Wylandriah",
                    "Klucz do pokoju Malurila", "Posąg Dibelli"]
        for index in range(1, len(categories)):
            self.driver.find_element_by_link_text(categories[index]).click()
            self.check_table_first_data(f"id_{categories[index].lower()}_tbody", expected[index])
            table = self.driver.find_element_by_id(f"id_{categories[index].lower()}_tbody")
            self.wait_for(lambda: table.find_element_by_tag_name("input").send_keys("1"))

        # After that he submit all of them
        self.wait_for(lambda: self.submit_items_table())

        # on screen he sees message that all codes will be shown on commands page
        wrappers = self.wait_for(lambda: self.driver.find_elements_by_class_name("alert-primary"))
        for wrapper in wrappers:
            if wrapper.is_displayed():
                self.assertEqual(wrapper.text, COMMANDS_SUCCESS_MESSAGE + "\n×")

        # he go to that page and there is list of commands for items.
        self.driver.find_element_by_link_text("Commands").click()
        commands_list = self.driver.find_element_by_id("id_commands_list").text
        expected = "Commands List:\nplayer.additem 01016FFF 1\nplayer.additem 0110EC8C 1\n" \
                   "player.additem 0110F7F5 1\nplayer.additem 01106E1B 1\nplayer.additem 0110394D 1\n" \
                   "player.additem 011076EC 1\nplayer.additem 01043E26 1\nplayer.additem 0110BEFF 1\n" \
                   "player.additem 0110CC6A 1"
        self.assertEqual(commands_list, expected)

    def test_chosen_items_are_chosen_after_change_page(self):
        # Foris chose some items
        table = self.wait_for(lambda: self.driver.find_element_by_id("id_weapons_tbody"))
        self.wait_for(lambda: table.find_element_by_tag_name("input").send_keys("5"))
        self.driver.find_element_by_link_text("Armors").click()

        table = self.wait_for(lambda: self.driver.find_element_by_id("id_armors_tbody"))
        table.find_element_by_tag_name("input").send_keys("2")
        self.wait_for(lambda: self.submit_items_table())

        # then he change page and come back to items page
        self.driver.find_element_by_link_text("Skills").click()
        self.wait_for(lambda: self.driver.find_element_by_link_text("Items").click())

        # all earlier chosen items are still chosen
        table = self.wait_for(lambda: self.driver.find_element_by_id("id_weapons_tbody"))
        self.assertEqual(
            table.find_element_by_tag_name("input").get_attribute("value"),
            "5"
        )

        self.driver.find_element_by_link_text("Armors").click()
        table = self.wait_for(lambda: self.driver.find_element_by_id("id_armors_tbody"))
        self.assertEqual(
            table.find_element_by_tag_name("input").get_attribute("value"),
            "2"
        )

    def test_can_toggle_hide_not_selected_items(self):
        # Foris select few items in items page

        # he decide that he want check if he chose correct items
        # so he click hide button

        # now he sees only selected items, 
        # all are correct so he press show button

        # and now he sees all items
        self.fail("Finish test!")
