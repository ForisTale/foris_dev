from django.test import TestCase
from django.http import QueryDict
from django.forms import ValidationError
from the_elder_commands.forms import PluginsForm, PluginVariantsForm, SelectedPluginsForm, ValidateSkills, \
    SkillsValidationError
from the_elder_commands.models import Plugins, PluginVariants
from the_elder_commands.inventory import ADD_PLUGIN_FILE_ERROR_MESSAGE, PLUGIN_TEST_DICT, DEFAULT_SKILL_POST, \
    PLUGINS_ERROR_STRING_IS_EMTPY, PLUGINS_ERROR_NAME_BECOME_EMPTY, INCORRECT_LOAD_ORDER, PLUGIN_TEST_EMPTY_DICT, \
    SKILLS_ERROR_DESIRED_LEVEL_RANGE, SKILLS_ERROR_NEW_VALUE_BIGGER, \
    SKILLS_ERROR_DESIRED_LEVEL, DEFAULT_SKILLS, \
    SKILLS_ERROR_MULTIPLIER, SKILLS_ERROR_BASE_SKILL, SKILLS_ERROR_DESIRED_SKILL
import copy


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


class ValidateSkillsTest(TestCase):

    class FakeRequest:
        def __init__(self):
            self.POST = QueryDict("", mutable=True)
            self.POST.update(DEFAULT_SKILL_POST)
            self.POST.update({
                "desired_level": "1",
                "priority_multiplier": "1.5",
                "illusion_base": "15",
                "illusion_new": "",
                "sneak_base": "15",
                "sneak_new": "25",
                "sneak_multiplier": "on",
                "fill_skills": "true"
            })
            self.session = {}

    class FakeValidateSkillsSelf:
        def __init__(self, request):
            self.request = request
            self.errors = []

    def setUp(self):
        super().setUp()
        self.maxDiff = None

    def test_is_valid(self):
        request = self.FakeRequest()
        form = ValidateSkills(request)
        self.assertTrue(form.is_valid())
        form.errors.append("Error!")
        self.assertFalse(form.is_valid())

    def test_desired_level_need_to_be_integer(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        cases = {"1": 1, "a": None, "1.2": None, "": None}
        for case, expected in cases.items():
            request.POST.update({"desired_level": case})
            value = ValidateSkills._desired_level_validation(fake_self)
            self.assertEqual(value, expected)

    def test_wrong_desired_level_give_correct_error(self):
        request = self.FakeRequest()
        request.POST.update({"desired_level": "a"})
        fake_self = self.FakeValidateSkillsSelf(request)
        ValidateSkills._desired_level_validation(fake_self)
        self.assertEqual(fake_self.errors, [SKILLS_ERROR_DESIRED_LEVEL])

    def test_desired_level_need_to_be_between_1_and_81(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        cases = {"1": 1, "81": 81, "82": None, "0": None, "-1": None}
        for case, expected in cases.items():
            request.POST.update({"desired_level": case})
            actual = ValidateSkills._desired_level_validation(fake_self)
            self.assertEqual(actual, expected, msg=f"Fail on {case}")

    def test_desired_level_range_give_correct_error(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        request.POST.update({"desired_level": "0"})
        ValidateSkills._desired_level_validation(fake_self)
        self.assertEqual(fake_self.errors, [SKILLS_ERROR_DESIRED_LEVEL_RANGE])

    def test_priority_multiplier_is_float(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        cases = {"1": 1, "a": None, "1.2": 1.2, "": None}
        for case, expected in cases.items():
            request.POST.update({"priority_multiplier": case})
            value = ValidateSkills._priority_multiplier_validation(fake_self)
            self.assertEqual(value, expected)

    def test_wrong_multiplier_give_correct_error(self):
        request = self.FakeRequest()
        request.POST.update({"priority_multiplier": "a"})
        fake_self = self.FakeValidateSkillsSelf(request)
        ValidateSkills._priority_multiplier_validation(fake_self)
        self.assertEqual(fake_self.errors, [SKILLS_ERROR_MULTIPLIER])

    def test_skills(self):
        request = self.FakeRequest()
        form = ValidateSkills(request)
        self.assertTrue(form.is_valid())
        skills = copy.deepcopy(DEFAULT_SKILLS)
        skills["Stealth"]["sneak"].update({"desired_value": 25, "multiplier": True})
        self.assertDictEqual(skills["Stealth"]["sneak"], form.skills["Stealth"]["sneak"])

    def test_desired_need_to_be_bigger(self):
        request = self.FakeRequest()
        request.POST.update({"sneak_base": "30"})
        form = ValidateSkills(request)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, [SKILLS_ERROR_NEW_VALUE_BIGGER.format(skill="Sneak")])

    def test_skills_have_bottom_and_upper_limit(self):
        cases = {"14": False, "15": True, "100": True, "101": False}
        for case, result in cases.items():
            request = self.FakeRequest()
            request.POST.update({"illusion_base": case})
            form = ValidateSkills(request)
            self.assertEqual(form.is_valid(), result, msg=f"Fail on {case}")
        for case, result in cases.items():
            request = self.FakeRequest()
            request.POST.update({"illusion_new": case})
            form = ValidateSkills(request)
            self.assertEqual(form.is_valid(), result, msg=f"Fail on {case}")

    def test_new_value_is_bigger(self):
        self.assertTrue(ValidateSkills.is_new_skill_bigger(1, 2))
        self.assertTrue(ValidateSkills.is_new_skill_bigger(2, 2))
        self.assertTrue(ValidateSkills.is_new_skill_bigger(1, ""))
        self.assertFalse(ValidateSkills.is_new_skill_bigger(2, 1))

    def test_form_has_own_copy_of_skills(self):
        request = self.FakeRequest()
        form = ValidateSkills(request)
        skills = DEFAULT_SKILLS

        self.assertNotEqual(form.skills, skills)

    def test_get_default_skill(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        actual = ValidateSkills._get_default_skill(self=fake_self, skill="sneak", skill_name="Sneak")
        self.assertEqual(actual, 15)

    def test_get_desired_skill(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        actual = ValidateSkills._get_desired_skill(self=fake_self, skill="sneak", skill_name="Sneak")
        self.assertEqual(actual, 25)

    def test_get_default_skill_validate_skill(self):
        request = self.FakeRequest()
        cases = {"15": True, "a": False, "": False, "1.5": False}
        for case, result in cases.items():
            request.POST.update({"sneak_base": case})
            fake_self = self.FakeValidateSkillsSelf(request)
            value = ValidateSkills._get_default_skill(self=fake_self, skill="sneak", skill_name="Sneak")
            self.assertEqual(ValidateSkills.is_valid(fake_self), result, msg=f"Fail on {case}")
            if not result:
                self.assertEqual(fake_self.errors, [SKILLS_ERROR_BASE_SKILL.format(skill="Sneak")])
            else:
                self.assertEqual(fake_self.errors, [])
                self.assertEqual(int(case), value)

    def test_get_desired_skill_validate_skill(self):
        request = self.FakeRequest()
        cases = {"15": True, "a": False, "": True, "1.5": False}
        for case, result in cases.items():
            request.POST.update({"sneak_new": case})
            fake_self = self.FakeValidateSkillsSelf(request)
            value = ValidateSkills._get_desired_skill(self=fake_self, skill="sneak", skill_name="Sneak")
            self.assertEqual(ValidateSkills.is_valid(fake_self), result, msg=f"Fail case {case}")
            if not result:
                self.assertEqual(fake_self.errors,
                                 [SKILLS_ERROR_DESIRED_SKILL.format(skill="Sneak")])
            else:
                self.assertEqual(fake_self.errors, [])
                self.assertEqual(case, str(value))

    def test_get_multiplier_skill(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        self.assertTrue(ValidateSkills._get_multiplier(self=fake_self, skill="sneak"))
        self.assertFalse(ValidateSkills._get_multiplier(self=fake_self, skill="illusion"))

    def test_get_fill_skills(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        self.assertTrue(ValidateSkills._get_fill_skills(fake_self))

    def test_get_fill_skills_is_false_by_default(self):
        request = self.FakeRequest()
        request.POST.pop("fill_skills")
        fake_self = self.FakeValidateSkillsSelf(request)
        self.assertFalse(ValidateSkills._get_fill_skills(fake_self))

    def test_can_save(self):
        request = self.FakeRequest()
        form = ValidateSkills(request)
        form.save()
        self.assertDictEqual(
            request.session,
            {"skills": form.skills, "desired_level": 1, "multiplier": 1.5, "fill_skills": "true"}
        )

    def test_save_only_if_valid(self):
        request = self.FakeRequest()
        form = ValidateSkills(request)
        form.errors.append("Error!")
        with self.assertRaises(SkillsValidationError):
            form.save()
