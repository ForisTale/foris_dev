from django.test import TestCase
from the_elder_commands.models import Plugins, PluginVariants, Weapons, Keys, Books, Ammo, Armors, Alchemy, \
    Miscellaneous, Ingredients, Scrolls, SoulsGems
from the_elder_commands.services import PluginsService, ItemsService, SkillsService, SpellsService, PerksService, \
    WordsOfPowerService
from the_elder_commands.inventory import DEFAULT_SKILLS, PLUGIN_TEST_DICT_ALTERED_BY_FORM
from the_elder_commands.utils import default_skills_race_update
from the_elder_commands.utils_for_tests import populate_plugins_table, set_up_default_nord
import copy


class PluginsServiceTest(TestCase):
    def setUp(self):
        super().setUp()
        for plugin_num in range(1, 3):
            plugin = Plugins.objects.create(name="test 0" + str(plugin_num), usable_name="test_0" + str(plugin_num))
            for index in range(1, 4):
                PluginVariants.objects.create(version="0." + str(index), language="english", is_esl=False,
                                              instance=plugin)
                if index == 2:
                    PluginVariants.objects.create(version="0." + str(index), language="polish", is_esl=True,
                                                  instance=plugin)

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

    def test_service_dont_pass_plugin_without_data(self):
        Plugins.objects.create(name="Fake!", usable_name="Fake")
        plugin_service = self.set_up_fake_request_and_return_plugin_service()
        self.assertEqual(len(plugin_service.all_plugins), 2)

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
    class FakeRequest:
        session = {
            "selected": [{
                "name": "test 01",
                "usable_name": "test_01",
                "version": "03",
                "is_esl": False,
                "language": "english",
                "load_order": "A5"
            }],
            "chosen_items": {"test_01": 1, "test_02": "2"}
        }

    def setUp(self):
        populate_plugins_table()
        self.maxDiff = None

    def test_service_pass_selected_plugins(self):
        request = self.FakeRequest()
        service = ItemsService(request, "WEAP")
        test_dict = copy.deepcopy(PLUGIN_TEST_DICT_ALTERED_BY_FORM.get("WEAP"))
        for item in test_dict:
            item.update({"form_id": f"A5{item.get('form_id', '')}", "plugin_name": "test 01", "quantity": "",
                         "selected": False})

        self.assertDictEqual({1: service.items}, {1: test_dict})

    def test_service_use_chosen_items(self):
        request = self.FakeRequest()
        service = ItemsService(request, "WEAP")
        self.assertEqual(service.chosen, {"test_01": 1, "test_02": "2"})

    def test_get_item_model(self):
        variant = PluginVariants.objects.first()
        self.assertEqual(ItemsService.get_item_model("WEAP", variant), Weapons.objects.get(variant=variant))
        self.assertEqual(ItemsService.get_item_model("ARMO", variant), Armors.objects.get(variant=variant))
        self.assertEqual(ItemsService.get_item_model("AMMO", variant), Ammo.objects.get(variant=variant))
        self.assertEqual(ItemsService.get_item_model("BOOK", variant), Books.objects.get(variant=variant))
        self.assertEqual(ItemsService.get_item_model("INGR", variant), Ingredients.objects.get(variant=variant))
        self.assertEqual(ItemsService.get_item_model("ALCH", variant), Alchemy.objects.get(variant=variant))
        self.assertEqual(ItemsService.get_item_model("MISC", variant), Miscellaneous.objects.get(variant=variant))
        self.assertEqual(ItemsService.get_item_model("KEYM", variant), Keys.objects.get(variant=variant))
        self.assertEqual(ItemsService.get_item_model("SCRL", variant), Scrolls.objects.get(variant=variant))
        self.assertEqual(ItemsService.get_item_model("SLGM", variant), SoulsGems.objects.get(variant=variant))


class SpellsServiceTest(TestCase):
    class FakeRequest:
        session = {
            "selected": [{
                "name": "test 01",
                "usable_name": "test_01",
                "version": "03",
                "is_esl": False,
                "language": "english",
                "load_order": "A5"
            }],
            "chosen_spells": {"A510FD5F": True}
        }

    def setUp(self):
        self.maxDiff = None
        populate_plugins_table()

    def test_service_pass_selected_plugins(self):
        test_dict = copy.deepcopy(PLUGIN_TEST_DICT_ALTERED_BY_FORM.get("SPEL"))
        spells = test_dict[0]
        spells.update({"form_id": f"A5{spells.get('form_id', '')}", "plugin_name": "test 01", "selected": None})
        request = self.FakeRequest()
        service = SpellsService(request, "alteration")
        self.assertEqual({1: [spells]}, {1: service.spells})

        destruction_spell = test_dict[1]
        destruction_spell.update({"form_id": f"A5{destruction_spell.get('form_id', '')}", "plugin_name": "test 01",
                                  "selected": True})
        request = self.FakeRequest()
        service = SpellsService(request, "destruction")
        self.assertDictEqual({1: [destruction_spell]}, {1: service.spells})

    def test_service_use_chosen_spells(self):
        request = self.FakeRequest()
        service = SpellsService(request, "alteration")
        self.assertEqual(service.chosen, {"A510FD5F": True})


class WordsOfPowerServiceTest(TestCase):
    class FakeRequest:
        session = {
            "selected": [{
                "name": "test 01",
                "usable_name": "test_01",
                "version": "03",
                "is_esl": False,
                "language": "english",
                "load_order": "A5"
            }],
            "chosen_other": {"wordA50602A4": "on"}
        }

    def setUp(self):
        self.maxDiff = None
        populate_plugins_table()

    def test_service_pass_selected_plugins(self):
        test_words = copy.deepcopy(PLUGIN_TEST_DICT_ALTERED_BY_FORM.get("WOOP"))
        selected = [None, "on"]
        for index, word in enumerate(test_words):
            word.update({"form_id": f"A5{word.get('form_id', '')}", "plugin_name": "test 01",
                         "selected": selected[index]})

        request = self.FakeRequest()
        service = WordsOfPowerService(request)
        self.assertEqual(test_words, service.words)

    def test_service_use_chosen_words(self):
        request = self.FakeRequest()
        service = WordsOfPowerService(request)
        self.assertEqual(service.chosen, {"wordA50602A4": "on"})


class PerksServiceTest(TestCase):
    class FakeRequest:
        session = {
            "selected": [{
                "name": "test 01",
                "usable_name": "test_01",
                "version": "03",
                "is_esl": False,
                "language": "english",
                "load_order": "A5"
            }],
            "chosen_other": {"perkA510FCFA": "on"}
        }

    def setUp(self):
        self.maxDiff = None
        populate_plugins_table()

    def test_service_pass_selected_plugins(self):
        test_words = copy.deepcopy(PLUGIN_TEST_DICT_ALTERED_BY_FORM.get("PERK"))
        selected = [None, "on"]
        for index, word in enumerate(test_words):
            word.update({"form_id": f"A5{word.get('form_id', '')}", "plugin_name": "test 01",
                         "selected": selected[index]})

        request = self.FakeRequest()
        service = PerksService(request)
        self.assertEqual(test_words, service.perks)

    def test_service_use_chosen_words(self):
        request = self.FakeRequest()
        service = PerksService(request)
        self.assertEqual(service.chosen, {"perkA510FCFA": "on"})


class SkillsServiceTest(TestCase):

    class FakeRequest:
        def __init__(self):
            self.session = {"skills": set_up_default_nord(), "desired_level": 1, "multiplier": 1.5, "race": "nord",
                            "fill_skills": "true"}

    def setUp(self):
        self.maxDiff = None

    @staticmethod
    def set_up_desire_skills_for_altmer():
        skills = default_skills_race_update("altmer")
        skills["Combat"]["twohanded"]["desired_value"] = 20
        skills["Stealth"]["speechcraft"]["desired_value"] = 20
        skills["Stealth"]["lightarmor"]["desired_value"] = 20
        return skills

    def test_service_can_get_race(self):
        request = self.FakeRequest()
        service = SkillsService(request)
        self.assertEqual(service.race, "nord")

    def test_service_can_get_data_from_session(self):
        request = self.FakeRequest()
        service = SkillsService(request)
        self.assertEqual(service.skills, set_up_default_nord())
        self.assertEqual(service.multiplier, 1.5)
        self.assertEqual(service.race, "nord")
        self.assertEqual(service.fill_skills, "true")
        self.assertEqual(service.desired_level, 1)
        self.assertEqual(service.default_level, 1)

    # noinspection PyTypeChecker
    def test_predict_level_by_default_level(self):
        request = self.FakeRequest()
        skills = request.session.get("skills")
        skills["Combat"]["marksman"]["default_value"] = 20
        skills["Stealth"]["sneak"]["default_value"] = 20
        skills["Stealth"]["alchemy"]["default_value"] = 20
        service = SkillsService(request)
        self.assertEqual(service.predict_level("default"), 3)

    def test_predict_level_by_desired_level(self):
        skills = self.set_up_desire_skills_for_altmer()
        request = self.FakeRequest()
        request.session.update({"skills": skills, "race": "altmer"})
        service = SkillsService(request)
        self.assertEqual(service.predict_level("desired"), 3)

    def test_desired_level_return_default_level_when_smaller_than_default(self):
        skills = self.set_up_desire_skills_for_altmer()
        request = self.FakeRequest()
        request.session.update({"skills": skills, "race": "altmer", "desired_level": 2})
        service = SkillsService(request)
        self.assertEqual(service.desired_level, 2)
        request.session.pop("fill_skills")
        service = SkillsService(request)
        self.assertEqual(service.desired_level, 3)

    def test_set_skills_to_desired_level(self):
        request = self.FakeRequest()
        request.session.update({"desired_level": 10})
        service = SkillsService(request)
        actual = service.skills
        self.assertEqual(actual["Combat"]["marksman"]["desired_value"], 21)
        self.assertEqual(actual["Combat"]["block"]["desired_value"], 26)
        self.assertEqual(actual["Combat"]["twohanded"]["desired_value"], 31)

    def test_desired_level_fill_skills_only_to_100(self):
        skills = self.set_up_desire_skills_for_altmer()
        skills["Magic"]["alteration"]["desired_value"] = 99
        request = self.FakeRequest()
        request.session.update({"skills": skills, "race": "altmer", "desired_level": 81})
        service = SkillsService(request)
        for skill_type in service.skills:
            for name in service.skills[skill_type]:
                self.assertEqual(
                    service.skills[skill_type][name]["desired_value"],
                    100
                )

    def test_desired_level_did_not_have_infinity_loop(self):
        skills = copy.deepcopy(DEFAULT_SKILLS)
        for skill_type in skills:
            for name in skills[skill_type]:
                skills[skill_type][name]["default_value"] = 99
        request = self.FakeRequest()
        request.session.update({"skills": skills, "race": "altmer", "desired_level": 81})
        SkillsService(request)
        self.assertTrue(True, "It's not looping!")

    def test_create_commands_list(self):
        skills = self.set_up_desire_skills_for_altmer()
        request = self.FakeRequest()
        request.session.update({"skills": skills, "race": "altmer", "desired_level": 3})
        service = SkillsService(request)

        commands_list = ["player.advskill twohanded 425", "player.advskill lightarmor 632",
                         "player.advskill speechcraft 7013"]
        self.assertEqual(service.commands_list(), commands_list)
        self.assertEqual(service.commands, commands_list)
