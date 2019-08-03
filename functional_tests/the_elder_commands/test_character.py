from functional_tests.the_elder_commands.tec_base import FunctionalTest

DEFAULT_SKILL = {
    "Magic": {
        "Alteration": 15,
        "Conjuration": 15,
        "Destruction": 15,
        "Enchanting": 15,
        "Illusion": 15,
        "Restoration": 15
    },
    "Combat": {
        "Archery": 15,
        "Block": 15,
        "Heavy Armor": 15,
        "One-handed": 15,
        "Smithing": 15,
        "Two-handed": 15,
    },
    "Stealth": {
        "Alchemy": 15,
        "Light Armor": 15,
        "Lockpicking": 15,
        "Pickpocket": 15,
        "Sneak": 15,
        "Speech": 15
    }
}


class CharacterTest(FunctionalTest):

    def test_default_look_and_valuesC(self):
        # Foris open The elder commands website.
        self.driver.get(self.live_server_url)

        # And in title sees website name.
        self.assertEqual(self.driver.title, "The Elder Commands")

        # On page he sees "chose race" button
        self.assertEqual(
            self.driver.find_element_by_id("id_chose_race_button").text,
            "Chose Race"
        )

        # with selected Nord.
        self.assertEqual(
            self.driver.find_element_by_id("id_race_name").text,
            "Nord"
        )

        # There is also skill list category,
        skill_table = self.driver.find_elements_by_tag_name("td")

        for category in DEFAULT_SKILL.keys():
            self.assertIn(
                category,
                skill_table
            )

        # with skills,

            for skill in DEFAULT_SKILL[category]:
                self.assertIn(
                    skill,
                    skill_table
                )

        # that every one of them has some values.
                self.assertNotEqual(
                    self.driver.find_element_by_name(f"id_{skill}_value"),
                    ""
                )

        # There are empty checkboxes next to values
                self.equal_find_element_by_id(f"id_{skill}_priority", "")

        # and adjustment priority with default value
        self.equal_find_element_by_id("id_priority_value", 2)

        # next to it are two boxes with calculated lvl
        self.equal_find_element_by_id("id_calculated_level", 1)

        # and desired lvl.
        self.equal_find_element_by_id("id_desired_level", "")

        # On the bottom is button with name calculate.
        self.equal_find_element_by_id("id_calculate_button", "Calculate")

        # There is also empty commands lists column.
        self.equal_find_element_by_id("id_commands_list", "")
