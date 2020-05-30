from django.test import TestCase
from django.http import QueryDict
from django.forms import ValidationError
from the_elder_commands.forms import SkillsForm, PluginsForm, PluginVariantsForm, SelectedPluginsForm
from the_elder_commands.models import Skills, Plugins, PluginVariants
from the_elder_commands.services import SkillsService
from the_elder_commands.inventory import ADD_PLUGIN_FILE_ERROR_MESSAGE, PLUGIN_TEST_DICT, \
    PLUGINS_ERROR_STRING_IS_EMTPY, PLUGINS_ERROR_NAME_BECOME_EMPTY, INCORRECT_LOAD_ORDER, PLUGIN_TEST_EMPTY_DICT
import copy


class SkillsFormTest(TestCase):

    def test_form_passes_data_to_model(self):
        instance = Skills.objects.get_or_create(session_key="key")[0]
        form = SkillsForm(data={"race": "Nord"}, instance=instance)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Skills.objects.count(), 1)
        self.assertEqual(
            Skills.objects.get(session_key="key"),
            Skills.objects.all()[0]
        )


class SkillsFormValidationTest(TestCase):
    def setUp(self):
        self.instance = Skills.objects.get_or_create(session_key="key")[0]

    def check_fail_and_message(self, form, error_message):
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            error_message
        )

    def test_desired_level_range(self):
        cases = [0, 82, -20]
        for case in cases:
            form = SkillsForm(data={"desired_level": str(case)}, instance=self.instance)
            self.check_fail_and_message(form, {"desired_level":
                                               ["The desired level need to be a integer between 1 and 81."]})
        form = SkillsForm(data={"desired_level": 5}, instance=self.instance)
        self.assertTrue(form.is_valid())

    def test_desired_level_is_number(self):
        form = SkillsForm(data={"desired_level": "ala"}, instance=self.instance)
        self.check_fail_and_message(form, {"desired_level":
                                           ["Enter a whole number."]})

    def test_priority_multiplier_is_number(self):
        form = SkillsForm(data={"priority_multiplier": "ala"}, instance=self.instance)
        self.check_fail_and_message(form, {'priority_multiplier': ['Enter a number.']})

    def test_skills_range(self):
        skills = SkillsService.default_race_skills_update("Nord")
        cases = ["14", "101", "-50"]
        for kind in ["default", "desired"]:
            for case in cases:
                skills["Magic"]["Alteration"][kind + "_value"] = case
                form = SkillsForm(data={"skills": skills}, instance=self.instance)
                self.check_fail_and_message(form, {'skills':
                                                   ['The skill need to be a integer between 15 and 100.']})
            skills["Magic"]["Alteration"][kind + "_value"] = "15"
            form = SkillsForm(data={"skills": skills}, instance=self.instance)
            self.assertTrue(form.is_valid())

    def test_skills_values_are_numbers(self):
        skills = SkillsService.default_race_skills_update("Nord")
        skills["Magic"]["Alteration"]["default_value"] = "test"
        skills["Magic"]["Alteration"]["desired_value"] = "test"
        form = SkillsForm(data={"skills": skills}, instance=self.instance)
        self.check_fail_and_message(form, {"skills":
                                           ['All skills values must be integers!']})

    def test_desired_must_be_bigger_than_default(self):
        skills = SkillsService.default_race_skills_update("Nord")
        skills["Magic"]["Alteration"]["default_value"] = 55
        skills["Magic"]["Alteration"]["desired_value"] = 35
        form = SkillsForm(data={"skills": skills}, instance=self.instance)
        self.check_fail_and_message(form, {'skills': ['New value of skills must be bigger than a value!']})

        skills["Magic"]["Alteration"]["desired_value"] = 56
        form = SkillsForm(data={"skills": skills}, instance=self.instance)
        self.assertTrue(form.is_valid())


class PluginsFormTest(TestCase):

    def test_form_pass_data_to_model(self):
        form = PluginsForm(name="test 01")
        self.assertTrue(form.is_valid())

        self.assertEqual(Plugins.objects.count(), 1)
        self.assertEqual(
            Plugins.objects.get(name="test 01"),
            Plugins.objects.all()[0]
        )

    def test_form_clean_name_and_create_usable_name_from_name(self):
        form = PluginsForm(name="Test 5'a <>[]{}()!@#$%^&*sony\"\' raw **")
        self.assertTrue(form.is_valid())

        plugins = Plugins.objects.first()
        self.assertEqual(plugins.name, "Test 5a sony raw ")
        self.assertEqual(plugins.usable_name, "test_5a_sony_raw_")

    def test_plugin_name_cannot_be_empty_string(self):
        form = PluginsForm(name="")
        self.assertEqual(len(Plugins.objects.all()), 0)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors[0], PLUGINS_ERROR_STRING_IS_EMTPY)

    def test_after_clean_name_and_usable_name_cannot_be_empty(self):
        form = PluginsForm(name="## #$")
        self.assertEqual(len(Plugins.objects.all()), 0)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors[0], PLUGINS_ERROR_NAME_BECOME_EMPTY)


class PluginFormValidationTest(TestCase):

    def setUp(self):
        empty_dict = QueryDict("", mutable=True)
        self.data = empty_dict.copy()
        self.data.update({"plugin": {
            "name": "test 01",
        }})
        corrected_dict = copy.deepcopy(PLUGIN_TEST_DICT)
        corrected_dict.pop("isEsl")
        self.data.update({"variant": {
            "version": "0.1",
            "language": "Polish",
            "is_esl": False,
            "plugin_data": corrected_dict,
        }})

    def count_plugins_or_variants(self, amount, plugins=True):
        form = PluginsForm(name=self.data["plugin"]["name"])
        self.assertTrue(form.is_valid())

        variant = PluginVariantsForm(data=self.data["variant"], instance=form.instance)
        if not variant.is_valid():
            print(variant.errors)
        variant.save()
        if plugins:
            self.assertEqual(len(Plugins.objects.all()), amount)
        else:
            self.assertEqual(len(Plugins.objects.all()), 1)
            self.assertEqual(len(PluginVariants.objects.filter(instance=form.instance)), amount)

    def test_plugin_data_do_not_take_empty_dict(self):
        self.data["variant"]["plugin_data"] = {}
        form = PluginsForm(name=self.data["plugin"]["name"])
        self.assertTrue(form.is_valid())

        variant_form = PluginVariantsForm(data=self.data["variant"], instance=form.instance)
        self.assertFalse(variant_form.is_valid())
        self.assertEqual(
            variant_form.errors,
            {"plugin_data": [ADD_PLUGIN_FILE_ERROR_MESSAGE]}
        )

    def test_plugin_data_have_correct_structure(self):
        self.data["variant"]["plugin_data"] = {"test": 1}

        form = PluginsForm(name=self.data["plugin"]["name"])
        variant_form = PluginVariantsForm(data=self.data["variant"], instance=form.instance)
        self.assertFalse(variant_form.is_valid())
        self.assertEqual(variant_form.errors, {"plugin_data": [ADD_PLUGIN_FILE_ERROR_MESSAGE]})

    def test_plugin_data_is_stripped_from_html_char(self):
        self.data["variant"]["plugin_data"] = PLUGIN_TEST_EMPTY_DICT
        self.data["variant"]["plugin_data"]["WEAP"].append({"name": "&<>test'\""})

        form = PluginsForm(name=self.data["plugin"]["name"])
        variant_form = PluginVariantsForm(data=self.data["variant"], instance=form.instance)
        variant_form.save()
        variant = PluginVariants.objects.first()
        weap_list = variant.plugin_data.get("WEAP")
        item = weap_list[0]
        tested_string = item.get("name")
        self.assertEqual("&amp;&lt;&gt;test&#39;&quot;", tested_string)

    def test_escape_items(self):
        items = [
            {"name": "&test",
             "other": ">some"},
        ]
        expected = [
            {"name": "&amp;test",
             "other": "&gt;some"},
        ]
        actual = PluginVariantsForm.escape_items(items)
        self.assertEqual(expected, actual)

    def test_escape_items_can_handle_wrong_data(self):
        cases = [None, [None], [{None}]]
        for case in cases:
            with self.assertRaises(ValidationError, msg=f"Fail on {case}"):
                PluginVariantsForm.escape_items(case)

    def test_unique_validation(self):
        plugin = Plugins.objects.create(name="test", usable_name="test")
        plugin.save()

        form = PluginVariantsForm(instance=plugin, data=self.data["variant"])
        self.assertTrue(form.is_valid())
        form.save()

        other_form = PluginVariantsForm(instance=plugin, data=self.data["variant"])
        self.assertFalse(other_form.is_valid())

        plugin = Plugins.objects.create(name="test 02", usable_name="test")
        another_form = PluginVariantsForm(instance=plugin, data=self.data["variant"])
        self.assertTrue(another_form.is_valid())

    def test_form_create_new_plugin_only_if_there_is_new_name(self):

        self.count_plugins_or_variants(1, plugins=True)

        self.data["plugin"].update({"name": "test 02"})

        self.count_plugins_or_variants(2, plugins=True)

        self.data["variant"].update({"version": "0.2"})

        self.count_plugins_or_variants(2, plugins=True)

    def test_form_create_plugins_variants_for_each_version(self):

        self.count_plugins_or_variants(1, plugins=False)

        self.data["variant"].update({"version": "0.2"})

        self.count_plugins_or_variants(2, plugins=False)

        self.data["variant"].update({"language": "English"})

        self.count_plugins_or_variants(3, plugins=False)

    def test_plugin_version_is_stripped_from_most_special_signs(self):
        self.data["variant"].update({"version": "a!@#$%^&*()_-=+;:\"\',<>./?`~\\|"})
        plugin = Plugins.objects.create(name="test", usable_name="test")
        form = PluginVariantsForm(instance=plugin, data=self.data["variant"])
        self.assertTrue(form.is_valid())
        form.save()
        plugin_variant = PluginVariants.objects.first()
        self.assertEqual(plugin_variant.version, "a_-;:,.")


class SelectPluginFormTest(TestCase):
    def setUp(self):
        self.data = QueryDict("", mutable=True)
        self.data.update({"selected": "test_01", "test_01_variant": "0.1&english&",
                          "test_02_variant": "0.2&english&esl", "test_01_load_order": "01",
                          "test_02_load_order": "FE001"})
        self.data.update({"selected": "test_02"})
        Plugins.objects.create(name="test 01", usable_name="test_01")
        Plugins.objects.create(name="test 02", usable_name="test_02")

    def test_validate_load_order_for_esp(self):
        cases = {"A1": True, "*s": False, "AA1": False, "": False, "3": False, "#": False, "FE001": False, "FE1": False}

        class FakeRequest:
            POST = self.data
            session = {}

        for case, result in cases.items():
            self.data["test_01_load_order"] = case
            form = SelectedPluginsForm(request=FakeRequest)
            self.assertEqual(form.is_valid(), result, msg=f"{case} {result} {form.errors}")
            if result is False:
                self.assertEqual(form.errors[0], INCORRECT_LOAD_ORDER)

    def test_validate_load_order_for_esl(self):
        cases = {"A1": False, "*s": False, "AA1": False, "": False, "3": False, "#": False, "FE001": True, "FE1": False,
                 "AB001": False, "FF001": True}

        class FakeRequest:
            POST = self.data
            session = {}

        for case, result in cases.items():
            self.data["test_02_load_order"] = case
            form = SelectedPluginsForm(request=FakeRequest)
            self.assertEqual(form.is_valid(), result, msg=f"{case} {result} {form.errors}")
            if result is False:
                self.assertEqual(form.errors[0], INCORRECT_LOAD_ORDER)

    def test_is_esl(self):
        class FakeRequest:
            POST = self.data
            session = {}

        form = SelectedPluginsForm(request=FakeRequest)
        self.assertEqual(form.is_esl("test_01"), False)
        self.assertEqual(form.is_esl("test_02"), True)

    def test_form_process_data(self):
        class FakeRequest:
            POST = self.data
            session = {}

        request = FakeRequest

        SelectedPluginsForm(request=request)
        expected = [{
            "name": "test 01",
            "usable_name": "test_01",
            "version": "0.1",
            "language": "english",
            "load_order": "01",
            "esl": "",
        }]
        self.assertDictEqual(request.session.get("selected", [])[0], expected[0])
        self.assertEqual(request.session.get("selected")[1].get("esl"), "esl")
