from functional_tests.the_elder_commands.tec_base import FunctionalTest
from the_elder_commands.inventory import DEFAULT_SKILLS


class CharacterTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        # Foris open The elder commands website.
        self.driver.get(self.live_server_url)

    def fill_default_values(self):
        self.driver.find_element_by_name("sneak_base").clear()
        self.driver.find_element_by_name("sneak_base").send_keys("30")
        self.driver.find_element_by_name("smithing_base").clear()
        self.driver.find_element_by_name("smithing_base").send_keys("22")
        self.driver.find_element_by_name("marksman_base").clear()
        self.driver.find_element_by_name("marksman_base").send_keys("26")

    def test_default_look_and_values(self):
        # And in title Foris sees website name.
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
        self.wait_for(lambda: self.equal_find_element_by_id("id_commands_list", "Commands List:"))

    def test_validation(self):
        # Then Foris write some letters into skills
        self.driver.find_element_by_name("block_base").send_keys("dfsds")
        self.driver.find_element_by_id("id_calculate").click()

        # Error appear.
        self.wait_for(lambda: self.assertIn(
            "All skills values must be integers!",
            self.driver.find_element_by_tag_name("body").text
        ))

        # So now he try give very large number into skill
        self.driver.find_element_by_name("block_base").send_keys("101")
        self.driver.find_element_by_id("id_calculate").click()

        # Again error appear
        self.wait_for(lambda: self.assertIn(
            "The skill need to be a integer between 15 and 100.",
            self.driver.find_element_by_tag_name("body").text
        ))

        # Not disheartened he try put value bigger than new value
        self.driver.find_element_by_name("block_base").clear()
        self.driver.find_element_by_name("block_base").send_keys("35")
        self.driver.find_element_by_name("block_new").send_keys("25")
        self.driver.find_element_by_id("id_calculate").click()

        # and error appear
        self.wait_for(lambda: self.assertIn(
            "New value of skills must be bigger than a value!",
            self.driver.find_element_by_tag_name("body").text
        ))

    def test_calculate_desired_level(self):
        # Foris set skills in value and new value
        self.driver.find_element_by_name("block_base").clear()
        self.driver.find_element_by_name("block_base").send_keys("35")
        self.driver.find_element_by_name("block_new").send_keys("55")
        # after click calculate
        self.driver.find_element_by_id("id_calculate").click()

        # desired level and calculated level are correct
        self.wait_for(lambda: self.assertEqual(
            self.driver.find_element_by_id("id_calculated_level").text,
            "Calculated level: 4"
        ))

        self.assertEqual(
            self.driver.find_element_by_name("desired_level").get_attribute("value"),
            "8"
        )

    def test_set_multiplier_and_desired_level_auto_fill_skills(self):
        # Foris set some skills multiplier as "on"
        cases = self.wait_for(lambda: [
            self.driver.find_element_by_name("block_multiplier"),
            self.driver.find_element_by_name("illusion_multiplier"),
            self.driver.find_element_by_name("alchemy_multiplier"),
        ])
        for case in cases:
            case.click()

        # change priority multiplier
        self.driver.find_element_by_name("priority_multiplier").clear()
        self.driver.find_element_by_name("priority_multiplier").send_keys("2")

        # put some default values
        self.fill_default_values()

        # set desired level
        self.driver.find_element_by_name("desired_level").clear()
        self.driver.find_element_by_name("desired_level").send_keys("20")

        # and check fill level
        self.driver.find_element_by_name("fill_skills").click()

        # and then submit form
        self.driver.find_element_by_id("id_calculate").click()

        # now he sees that desired skills change
        self.wait_for(lambda: self.assertNotEqual(
            self.driver.find_element_by_name("sneak_new").get_attribute("value"),
            ""
        ))

        # multiplier are still checked
        cases = self.wait_for(lambda: [
            self.driver.find_element_by_name("block_multiplier"),
            self.driver.find_element_by_name("illusion_multiplier"),
            self.driver.find_element_by_name("alchemy_multiplier"),
        ])
        for case in cases:
            self.wait_for(lambda: self.assertEqual(case.is_selected(), True))

        # and commands list is full of commands
        list_of_commands = self.driver.find_element_by_id("id_commands_list") \
            .find_elements_by_tag_name("td")
        list_of_commands = [row.text for row in list_of_commands]
        self.assertNotEqual(
            list_of_commands,
            []
        )

    def test_calculate_default_level(self):
        # Foris set some of default values
        self.wait_for(lambda: self.fill_default_values())
        # send form
        self.driver.find_element_by_id("id_calculate").click()
        # and default level changed
        self.wait_for(lambda: self.equal_find_element_by_id("id_calculated_level",
                                                            "Calculated level: 5"))
        self.assertEqual(
            self.driver.find_element_by_id("id_desired_level").get_attribute("value"),
            "5"
        )

    def test_calculate_desired_level_and_skills(self):
        # Foris change race to orc
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
            "player.advskill alteration 842",
            "player.advskill speechcraft 7013",
            "player.advskill lightarmor 632",
        ]
        self.assertEqual(commands, list_of_commands)
