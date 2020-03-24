from functional_tests.the_elder_commands.tec_base import FunctionalTest
from the_elder_commands.inventory import DEFAULT_SKILLS


class BaseLooksTest(FunctionalTest):
    def setUp(self):
        super().setUp()

        # Foris open The Elder Commands website.
        self.driver.get(self.live_server_url)

    def test_items_looks(self):
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
        self.fail("Finish test!")

    def test_look_and_values(self):
        # On page he sees "Reset & Change Race" button
        self.assertEqual(
            self.driver.find_element_by_tag_name("button").text,
            "Reset & Change Race"
        )

        # with selected Nord.
        self.equal_find_element_by_id("id_race_name", "Chosen race:\nNord")

        # There is also skill list category,
        for category in DEFAULT_SKILLS.keys():
            skill_table = self.driver.find_elements_by_tag_name("th")
            skill_table = [row.text for row in skill_table]

            self.assertIn(
                category,
                skill_table
            )

            # with skills,
            skill_table = self.driver.find_elements_by_tag_name("td")
            skill_table = [row.text for row in skill_table]

            for skill, items in DEFAULT_SKILLS[category].items():
                self.assertIn(
                    skill,
                    skill_table
                )

                # that every one of them has some values.
                skill_value = 15
                if skill == "Two-handed":
                    skill_value += 10
                elif skill in ["Block", "Light Armor",
                               "One-handed", "Smithing",
                               "Speech"]:
                    skill_value += 5
                base_value = self.driver.find_element_by_name(f"{items['console_name']}_base")
                self.assertEqual(
                    base_value.get_attribute("value"),
                    str(skill_value)
                )

                # There are empty checkboxes next to values
                self.assertEqual(
                    self.driver.find_element_by_name(f"{items['console_name']}_multiplier")
                        .get_attribute("value"),
                    "on"
                )

                # and place for skill new value
                self.assertEqual(
                    self.driver.find_element_by_name(f"{items['console_name']}_new").text,
                    ""
                )

        # Below is adjustment multiplier
        self.equal_find_element_by_id("id_multiplier", "")

        # next to it are two boxes with calculated lvl
        self.equal_find_element_by_id("id_calculated_level", "Calculated level: 1")

        # and desired lvl.
        self.equal_find_element_by_id("id_desired_level", "")

        # On the bottom is button with name calculate.
        self.assertEqual(
            self.driver.find_elements_by_tag_name("button")[-1].text,
            "Calculate"
        )

        # There is also empty commands lists column.
        self.equal_find_element_by_id("id_commands_list", "Commands List:")
