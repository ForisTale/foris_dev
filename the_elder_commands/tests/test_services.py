from django.test import TestCase
from the_elder_commands.models import Skills, Plugins, PluginVariants
from the_elder_commands.services import SkillsService, PluginsService, ItemsService
from the_elder_commands.inventory import DEFAULT_SKILLS, PLUGIN_TEST_DICT
from functional_tests.the_elder_commands import test_plugins
import copy


class SkillsServiceTest(TestCase):

    @staticmethod
    def set_up_default_nord():
        skills = copy.deepcopy(DEFAULT_SKILLS)
        skills["Combat"]["Two-handed"]["default_value"] += 10
        skills["Stealth"]["Speech"]["default_value"] += 5
        skills["Stealth"]["Light Armor"]["default_value"] += 5
        for skill in ["Block", "One-handed", "Smithing"]:
            skills["Combat"][skill]["default_value"] += 5
        return skills

    @staticmethod
    def set_up_desire_skills():
        skills = SkillsService.default_race_skills_update("Altmer")
        skills["Combat"]["Two-handed"]["desired_value"] = 20
        skills["Stealth"]["Speech"]["desired_value"] = 20
        skills["Stealth"]["Light Armor"]["desired_value"] = 20
        Skills.objects.create(race="Altmer", session_key="key", skills=skills)
        character = SkillsService("key")
        return character

    def test_race_skills_update_depend_on_race(self):
        default_skills = SkillsService.default_race_skills_update("Nord")
        skills = self.set_up_default_nord()
        self.assertEqual(default_skills, skills)

    def test_predict_level(self):
        skills = self.set_up_default_nord()
        skills["Combat"]["Archery"]["default_value"] = 20
        skills["Stealth"]["Sneak"]["default_value"] = 20
        skills["Stealth"]["Alchemy"]["default_value"] = 20
        Skills.objects.create(session_key="key", skills=skills)
        self.assertEqual(
            SkillsService(session_key="key").default_level,
            3
        )

    def test_commands_list(self):
        character = self.set_up_desire_skills()
        commands_list = [
            "player.advskill twohanded 425",
            "player.advskill speechcraft 7013",
            "player.advskill lightarmor 632",
        ]
        self.assertEqual(character.commands_list(), commands_list)

    def test_predict_desired_level_count_from_default(self):
        skills = copy.deepcopy(DEFAULT_SKILLS)
        skills["Magic"]["Alteration"]["default_value"] = 32
        skills["Magic"]["Alteration"]["desired_value"] = 40
        skills["Magic"]["Enchanting"]["default_value"] = 40
        Skills.objects.create(session_key="key", skills=skills)
        character = SkillsService(session_key="key")
        self.assertEqual(character.default_level, 7)
        self.assertEqual(character.desired_level, 8)

    def test_if_passes_non_exist_session_key_create_default(self):
        SkillsService(session_key="key")
        character = Skills.objects.first()
        self.assertEqual(character.session_key, "key")

    def test_desired_skills_update_return_correct_object(self):
        character = self.set_up_desire_skills()
        self.assertEqual(
            character.skills["Stealth"]["Speech"]["desired_value"],
            20
        )

    def test_empty_character_desired_skills_return_desired_skills_empty_value(self):
        character = SkillsService(session_key="key")
        self.assertEqual(
            character.skills["Magic"]["Alteration"]["desired_value"],
            ""
        )

    def test_desired_level_is_calculated_against_default_skills(self):
        skills = self.set_up_default_nord()
        skills["Combat"]["One-handed"]["default_value"] = 25
        skills["Combat"]["One-handed"]["desired_value"] = 35
        Skills.objects.create(session_key="key", skills=skills)
        character = SkillsService(session_key="key")
        self.assertEqual(character.default_level, 2)
        self.assertEqual(character.desired_level, 4)

    def test_calculate_desired_level(self):
        character = self.set_up_desire_skills()
        self.assertEqual(character.desired_level, 3)
        model = Skills.objects.get(session_key="key")
        model.desired_level = 6
        model.fill_skills = True
        model.save()
        changed_character = SkillsService(session_key="key")
        self.assertEqual(changed_character.desired_level, 6)

    def test_if_desired_level_is_bigger_than_calculated_then_change_skills(self):
        self.set_up_desire_skills()
        model = Skills.objects.get(session_key="key")
        model.desired_level = 6
        model.fill_skills = True
        model.save()
        character = SkillsService(session_key="key")
        cases = [
            character.skills["Combat"]["Archery"]["desired_value"],
            character.skills["Combat"]["Block"]["desired_value"],
            character.skills["Stealth"]["Alchemy"]["desired_value"],
        ]
        for case in cases:
            self.assertNotEqual(case, "")
            self.assertNotEqual(case, 15)

    def test_desired_level_fill_skills_only_to_100(self):
        self.set_up_desire_skills()
        model = Skills.objects.get(session_key="key")
        model.desired_level = 81
        model.fill_skills = True
        skills = model.skills
        skills["Magic"]["Alteration"]["desired_value"] = 99
        model.save()

        character = SkillsService(session_key="key")
        for skill_type in character.skills:
            for name in character.skills[skill_type]:
                self.assertEqual(
                    character.skills[skill_type][name]["desired_value"],
                    100
                )

    def test_desired_level_did_not_have_infinity_loop(self):
        skills = copy.deepcopy(DEFAULT_SKILLS)
        categories = ["Magic", "Combat", "Stealth"]
        skills_categories = [['Alteration', 'Conjuration', 'Destruction', 'Enchanting', 'Illusion', 'Restoration'],
                             ['Archery', 'Block', 'Heavy Armor', 'One-handed', 'Smithing', 'Two-handed'],
                             ['Alchemy', 'Light Armor', 'Lockpicking', 'Pickpocket', 'Sneak', 'Speech']]
        for index in range(3):
            for skill in skills_categories[index]:
                skills[categories[index]][skill]["default_value"] = 99
        Skills.objects.update_or_create(session_key="key", skills=skills, desired_level=81, fill_skills=True)
        SkillsService(session_key="key")
        self.assertTrue(True, "It's not looping!")


class PluginsServiceTest(TestCase):
    def setUp(self):
        super().setUp()
        for plugin_num in range(1, 3):
            plugin = Plugins.objects.create(name="test 0" + str(plugin_num), usable_name="test_0" + str(plugin_num))
            for index in range(1, 4):
                PluginVariants.objects.create(version="0." + str(index), language="english", is_esl=False,
                                              plugin_data={"test": index}, instance=plugin)
                if index == 2:
                    PluginVariants.objects.create(version="0." + str(index), language="polish", is_esl=True,
                                                  plugin_data={"test": index}, instance=plugin)

    def set_up_fake_request_and_return_plugin_service(self):
        class Request:
            def __init__(self):
                self.session = {"selected": [{
                    "name": "test 01",
                    "usable_name": "test_01",
                    "version": "0.3",
                    "is_esl": "",
                    "language": "english",
                    "load_order": "FF"
                }]}

        return PluginsService(request=Request())

    def test_get_all_plugins_return_all_plugins_from_database(self):

        plugin_service = self.set_up_fake_request_and_return_plugin_service()
        all_plugins = plugin_service.all_plugins
        self.assertEqual(len(all_plugins), 2)

        actual = all_plugins[0]
        self.assertIsInstance(actual, PluginsService.Plugin)
        self.assertEqual(actual.name, "test 01")
        self.assertEqual(actual.usable_name, "test_01")
        self.assertEqual(actual.load_order, "FF")
        self.assertEqual(actual.selected, True)
        self.assertEqual(len(actual.variants), 4)
        self.assertEqual(actual.variants[0].language, "english")
        self.assertEqual(actual.variants[0].version, "0.3")
        self.assertEqual(actual.variants[0].selected, True)
        self.assertEqual(actual.variants[0].esl, "")
        self.assertEqual(actual.variants[1].selected, False)
        self.assertEqual(actual.variants[2].esl, "esl")
        actual = all_plugins[1]
        self.assertIsInstance(actual, PluginsService.Plugin)
        self.assertEqual(actual.name, "test 02")
        self.assertEqual(actual.usable_name, "test_02")
        self.assertEqual(actual.load_order, "")
        self.assertEqual(actual.selected, False)
        self.assertEqual(len(actual.variants), 4)
        self.assertEqual(actual.variants[0].language, "english")
        self.assertEqual(actual.variants[0].version, "0.3")
        self.assertEqual(actual.variants[0].esl, "")
        self.assertEqual(actual.variants[0].selected, False)
        self.assertEqual(actual.variants[1].selected, False)
        self.assertEqual(actual.variants[2].esl, "esl")

    def test_is_plugin_selected(self):

        plugin_service = self.set_up_fake_request_and_return_plugin_service()
        self.assertEqual(True, plugin_service.is_plugin_selected("test 01"))
        self.assertEqual(False, plugin_service.is_plugin_selected("test 02"))
        self.assertEqual(False, plugin_service.is_plugin_selected("test"))

    def test_get_load_order(self):
        plugin_service = self.set_up_fake_request_and_return_plugin_service()
        self.assertEqual("FF", plugin_service.get_load_order("test 01"))
        self.assertEqual("", plugin_service.get_load_order("test 02"))
        self.assertEqual("", plugin_service.get_load_order("test"))

    def test_get_variants_return_list_of_variant_object(self):
        plugin_service = self.set_up_fake_request_and_return_plugin_service()
        actual = plugin_service.get_variants("test 01")
        self.assertEqual(len(actual), 4)
        self.assertIsInstance(actual[0], PluginsService.Variant)
        self.assertEqual(actual[0].language, "english")
        self.assertEqual(actual[0].version, "0.3")
        self.assertEqual(actual[0].selected, True)
        self.assertEqual(actual[0].esl, "")
        self.assertEqual(actual[1].selected, False)
        self.assertEqual(actual[2].esl, "esl")

    def test_get_variants_is_ordered_by_desc_version_and_asc_language(self):
        plugin_service = self.set_up_fake_request_and_return_plugin_service()
        actual = plugin_service.get_variants("test 01")
        self.assertEqual(actual[0].language, "english")
        self.assertEqual(actual[0].version, "0.3")
        self.assertEqual(actual[1].language, "english")
        self.assertEqual(actual[1].version, "0.2")
        self.assertEqual(actual[2].language, "polish")
        self.assertEqual(actual[2].version, "0.2")
        self.assertEqual(actual[3].language, "english")
        self.assertEqual(actual[3].version, "0.1")

    def test_is_variant_selected(self):
        plugin_service = self.set_up_fake_request_and_return_plugin_service()
        variants = PluginVariants.objects.filter(instance__name="test 01").order_by("-version")
        self.assertEqual(plugin_service.is_variant_selected(variants[0]), True)
        self.assertEqual(plugin_service.is_variant_selected(variants[1]), False)

    def test_is_variant_selected_return_true_only_for_correct_plugin(self):
        plugin_service = self.set_up_fake_request_and_return_plugin_service()
        variants = PluginVariants.objects.filter(instance__name="test 02").order_by("-version")
        self.assertEqual(plugin_service.is_variant_selected(variants[0]), False)
        self.assertEqual(plugin_service.is_variant_selected(variants[1]), False)


class ItemsServiceTest(TestCase):
    def setUp(self):
        test_plugins.AddPluginTest.populate_plugins_table()
        self.maxDiff = None

    def test_service_pass_selected_plugins(self):

        class FakeRequest:
            session = {"selected": [{
                "name": "test 01",
                "usable_name": "test_01",
                "version": "03",
                "esl": False,
                "language": "english",
                "load_order": "A5"
            }]}

        service = ItemsService(FakeRequest, "WEAP")
        test_dict = copy.deepcopy(PLUGIN_TEST_DICT.get("WEAP"))
        for item in test_dict:
            item.update({"formId": f"A5{item.get('formId', '')}", "plugin_name": "test 01", "quantity": "",
                         "selected": False})

        self.assertDictEqual({1: service.items}, {1: test_dict})

    def test_get_items_run_only_when_change_in_selected(self):
        self.fail("Finish test!")

    def test_service_pass_chosen_items_into_template(self):

        class FakeRequest:
            session = {"chosen_items": {"test_01": 1, "test_02": "2"}}

        service = ItemsService(FakeRequest, "WEAP")
        self.assertEqual(service.chosen, {"test_01": 1, "test_02": "2"})

    def test_if_no_items_commands_return_empty_dict(self):

        class FakeRequest:
            session = {}

        service = ItemsService(FakeRequest, "WEAP")
        self.assertEqual(service.chosen, {})
