from functional_tests.the_elder_commands.tec_base import FunctionalTest
from the_elder_commands.inventory import DEFAULT_SKILLS
import time


class CharacterTest(FunctionalTest):

    def test_default_look_and_values(self):
        # Foris open The elder commands website.
        self.driver.get(self.live_server_url)

        # And in title sees website name.
        self.assertEqual(self.driver.title, "The Elder Commands")

        # On page he sees "chose race" button
        self.assertEqual(
            self.driver.find_element_by_tag_name("button").text,
            "Chose Race"
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
                self.equal_find_element_by_id(f"id_{items['console_name']}_priority", "")

        # and place for skill new value
                self.assertEqual(
                    self.driver.find_element_by_name(f"{items['console_name']}_new").text,
                    ""
                )

        # Below is adjustment priority
        self.equal_find_element_by_id("id_priority_multiplier", "")

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

    def test_calculate_level(self):
        # Foris open the elder commands website.
        self.driver.get(self.live_server_url)

        # He change race to orc
        self.driver.find_element_by_id("id_chose_race").click()
        self.driver.find_element_by_class_name("ork_race").click()

        self.equal_find_element_by_id("id_race_name", "Chosen race:\nOrk")

        # and then skill value change.
        for category in DEFAULT_SKILLS.keys():
            for skill, items in DEFAULT_SKILLS[category].items():
                skill_value = 15
                if skill == "Heavy Armor":
                    skill_value += 10
                elif skill in ["Block", "Enchanting",
                               "One-handed", "Smithing",
                               "Two-handed"]:
                    skill_value += 5
                base_value = self.driver.find_element_by_name(f"{items['console_name']}_base")
                self.wait_for(lambda: self.assertEqual(
                    base_value.get_attribute("value"),
                    str(skill_value)
                ))

        # Foris set new value for some skills
        new_values = self.driver.find_elements_by_class_name("new_values")
        for new_value in new_values:
            if new_value.get_attribute("name") in ["alteration_new",
                                                   "speechcraft_new",
                                                   "lightarmor_new"]:
                new_value.send_keys(20)

        # and then press calculate.
        self.driver.find_element_by_id("id_calculate").click()

        # in desired level value changed
        self.wait_for(lambda: self.assertEqual(
            self.driver.find_element_by_name("desired_level").get_attribute("value"),
            "3"
        ))

        # and in commands list he sees list of commands
        list_of_commands = self.driver.find_element_by_id("id_commands_list")\
            .find_elements_by_tag_name("td")
        list_of_commands = [row.text for row in list_of_commands]
        commands = [
            "player.advskill alteration 2132",
            "player.advskill speechcraft 2132",
            "player.advskill lightarmor 2132",
        ]
        self.assertEqual(commands, list_of_commands)

