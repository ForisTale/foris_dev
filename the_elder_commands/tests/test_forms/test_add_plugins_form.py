import copy
from io import StringIO, BytesIO
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.http import QueryDict
from django.test import TestCase

from the_elder_commands.forms.add_plugins_form import AddPluginsForm, PluginVariantsForm, escape_html_for_forms, \
    get_data, get_cleaned_data, WeaponsForm, ArmorsForm, AmmoForm, AlchemyForm, BooksForm, IngredientsForm, \
    MiscellaneousForm, KeysForm, ScrollsForm, SoulsGemsForm, BaseItemsForm, PerksForm, WordsOfPowerForm, SpellsForm, \
    AlterationSpellsForm, ConjurationSpellsForm, DestructionSpellsForm, IllusionSpellsForm, RestorationSpellsForm, \
    OtherSpellsForm, BaseSpellForm
from the_elder_commands.inventory.messages import PLUGINS_ERROR_NAME_IS_EMTPY, PLUGINS_ERROR_NAME_BECOME_EMPTY, \
    ADD_PLUGIN_ERROR_FILE
from the_elder_commands.inventory.plugin_test import PLUGIN_TEST_FILE, PLUGIN_TEST_DICT
from the_elder_commands.models import Plugins, PluginVariants, Weapons, Armors, Books, Ingredients, Alchemy, \
    Miscellaneous, Ammo, Scrolls, SoulsGems, Keys, AlterationSpells, ConjurationSpells, DestructionSpells, \
    IllusionSpells, RestorationSpells, OtherSpells, Perks, WordsOfPower


class AddPluginsFormTest(TestCase):

    class FakeRequest:
        def __init__(self):
            self.POST = QueryDict("", mutable=True)
            self.POST.update({"plugin_version": "01", "plugin_language": "english"})

    class FakeSelf:
        def __init__(self):
            self.errors = []

    def test_form_pass_data_to_model(self):
        with StringIO(PLUGIN_TEST_FILE) as file:
            request = self.FakeRequest()
            request.FILES = {"plugin_file": file}
            request.POST.update({"plugin_name": "test 01"})
            form = AddPluginsForm(request)
            self.assertTrue(form.is_valid())

            self.assertEqual(Plugins.objects.count(), 1)
            self.assertEqual("test 01", Plugins.objects.first().name)
            self.assertEqual(PluginVariants.objects.count(), 1)
            self.assertEqual(PluginVariants.objects.first().instance.name, "test 01")

    def test_form_clean_name_and_create_usable_name_from_name(self):
        with StringIO(PLUGIN_TEST_FILE) as file:
            request = self.FakeRequest()
            request.POST.update({"plugin_name": "Test 5'a <>[]{}()!@#$%^&*sony\"\' raw **"})
            request.FILES = {"plugin_file": file}
            form = AddPluginsForm(request)
            self.assertTrue(form.is_valid())

            plugins = Plugins.objects.first()
            self.assertEqual(plugins.name, "Test 5a sony raw ")
            self.assertEqual(plugins.usable_name, "test_5a_sony_raw_")

    def test_plugin_name_cannot_be_empty_string(self):
        with StringIO(PLUGIN_TEST_FILE) as file:
            request = self.FakeRequest()
            request.FILES = {"plugin_file": file}
            request.POST.update({"plugin_name": ""})
            form = AddPluginsForm(request)
            self.assertEqual(len(Plugins.objects.all()), 0)
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors, [PLUGINS_ERROR_NAME_IS_EMTPY])

    def test_after_clean_name_and_usable_name_cannot_be_empty(self):
        with StringIO(PLUGIN_TEST_FILE) as file:
            request = self.FakeRequest()
            request.FILES = {"plugin_file": file}
            request.POST.update({"plugin_name": "## #$"})
            form = AddPluginsForm(request)
            self.assertEqual(len(Plugins.objects.all()), 0)

            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors, [PLUGINS_ERROR_NAME_BECOME_EMPTY])

    def test_can_process_file_into_dict(self):
        with StringIO(PLUGIN_TEST_FILE) as file:
            request = self.FakeRequest()
            request.FILES = {"plugin_file": file}
            fake_self = self.FakeSelf()
            fake_self.request = request

            actual = AddPluginsForm.extract_dict_from_plugin_file(fake_self)

            self.maxDiff = None
            self.assertDictEqual(actual, PLUGIN_TEST_DICT)

    def test_catch_json_decode_error(self):
        with StringIO(" ") as file:
            request = self.FakeRequest()
            request.FILES = {"plugin_file": file}
            fake_self = self.FakeSelf()
            fake_self.request = request
            result = AddPluginsForm.extract_dict_from_plugin_file(fake_self)  # Should not raises!
        self.assertEqual(result, None)

    def test_catch_json_attribute_error(self):
        request = self.FakeRequest()
        request.FILES = {"plugin_file": {"plugin_file": 1}}
        fake_self = self.FakeSelf()
        fake_self.request = request

        result = AddPluginsForm.extract_dict_from_plugin_file(fake_self)  # Should not raises!
        self.assertEqual(result, None)

    def test_catch_unicode_error(self):
        with BytesIO(b"\x81") as file:
            request = self.FakeRequest()
            request.FILES = {"plugin_file": file}
            fake_self = self.FakeSelf()
            fake_self.request = request
            result = AddPluginsForm.extract_dict_from_plugin_file(fake_self)  # Should not raises!
        self.assertEqual(result, None)

    @patch("the_elder_commands.forms.add_plugins_form.AddPluginsForm.extract_dict_from_plugin_file")
    @patch("the_elder_commands.forms.add_plugins_form.AddPluginsForm.pop_is_esl")
    def test_extract_dict_pass_all_data_correctly(self, esl_mock, extract_mock):
        esl_mock.return_value = False
        extract_mock.return_value = {"data"}
        with StringIO(PLUGIN_TEST_FILE) as file:
            request = self.FakeRequest()
            request.FILES = {"plugin_file": file}
            fake_self = self.FakeSelf()
            fake_self.request = request
            fake_self.instance = ""
            fake_self.extract_dict_from_plugin_file = AddPluginsForm.extract_dict_from_plugin_file
            fake_self.pop_is_esl = AddPluginsForm.pop_is_esl

            post = AddPluginsForm.create_variants_post(fake_self)
            self.assertEqual(post.get("version"), "01")
            self.assertEqual(post.get("language"), "english")
            self.assertEqual(post.get("is_esl"), False)
            self.assertEqual(post.get("instance"), "")
            self.assertEqual(post.get("plugin_data"), {"data"})

    def test_pop_is_esl_from_dict(self):
        dictionary = {"test": 1, "isEsl": True}
        expected = {"test": 1}

        result = AddPluginsForm.pop_is_esl(dictionary)
        self.assertDictEqual(dictionary, expected)
        self.assertEqual(result, True)

    def test_pop_is_esl_can_handle_key_error_then_return_none(self):
        dictionary = {"test": 1}
        result = AddPluginsForm.pop_is_esl(dictionary)
        self.assertEqual(result, None)

    def test_pop_is_esl_can_handle_none_as_argument_then_return_none(self):
        dictionary = None
        result = AddPluginsForm.pop_is_esl(dictionary)
        self.assertEqual(result, None)

    def test_handle_data_form_save_data(self):
        fake_self = self.FakeSelf()
        fake_self.all_items_are_empty = AddPluginsForm.all_items_are_empty
        items_models = [Weapons, Armors, Books, Ingredients, Alchemy, Miscellaneous, Ammo, Scrolls, SoulsGems, Keys]
        spells_models = [AlterationSpells, ConjurationSpells, DestructionSpells,
                         IllusionSpells, RestorationSpells, OtherSpells]
        plugin = Plugins.objects.create(name="Some")
        variant = PluginVariants.objects.create(instance=plugin)
        data = {"plugin_data": copy.deepcopy(PLUGIN_TEST_DICT)}
        AddPluginsForm.handle_data_forms(fake_self, data, variant)
        for model in items_models:
            self.assertEqual(1, model.objects.count(), msg=f"Fail on {model}")
            self.assertNotEqual([], model.objects.first().items, msg=f"Fail on {model}")

        self.assertEqual(1, Perks.objects.count())
        self.assertNotEqual([], Perks.objects.first().perks)
        self.assertEqual(1, WordsOfPower.objects.count())
        self.assertNotEqual([], WordsOfPower.objects.first().words)
        for model in spells_models:
            self.assertEqual(1, model.objects.count(), msg=f"Fail on {model}")
            self.assertNotEqual([], model.objects.first().spells, msg=f"Fail on {model}")

    def test_handle_data_pass_error_when_forms_are_not_valid(self):
        with StringIO("""{\"isEsl\": 1, \"WEAP\": 1}""") as file:
            request = self.FakeRequest()
            request.FILES = {"plugin_file": file}
            request.POST.update({"plugin_name": "test 01"})
            form = AddPluginsForm(request)
        self.assertEqual(form.errors, [ADD_PLUGIN_ERROR_FILE])

    def test_if_all_empty_then_send_error(self):
        with StringIO("""{\"isEsl\": 1}""") as file:
            request = self.FakeRequest()
            request.FILES = {"plugin_file": file}
            request.POST.update({"plugin_name": "test 01"})
            form = AddPluginsForm(request)
        self.assertEqual(form.errors, [ADD_PLUGIN_ERROR_FILE])

    def test_all_items_are_empty(self):
        some_data = {"WEAP": ["1"], "ARMO": ["1"], "BOOK": ["1"], "INGR": ["1"], "ALCH": ["1"], "MISC": ["1"],
                     "PERK": ["1"], "AMMO": ["1"], "SCRL": ["1"], "SLGM": ["1"], "KEYM": ["1"], "SPEL": ["1"],
                     "WOOP": ["1"]}
        self.assertFalse(AddPluginsForm.all_items_are_empty(some_data))
        empty_data = {}
        self.assertTrue(AddPluginsForm.all_items_are_empty(empty_data))
        mix_data = {"WEAP": ["1"], "ARMO": ["1"], "WOOP": ["1"]}
        self.assertFalse(AddPluginsForm.all_items_are_empty(mix_data))

    def test_handle_data_form_delete_variant_if_all_empty(self):
        with StringIO("""{\"isEsl\": 1}""") as file:
            request = self.FakeRequest()
            request.FILES = {"plugin_file": file}
            request.POST.update({"plugin_name": "test 01"})
            AddPluginsForm(request)
        self.assertEqual(PluginVariants.objects.count(), 0)

    def test_handle_data_form_delete_variant_if_forms_dont_valid(self):
        with StringIO("""{\"isEsl\": 1, \"WEAP\": 1}""") as file:
            request = self.FakeRequest()
            request.FILES = {"plugin_file": file}
            request.POST.update({"plugin_name": "test 01"})
            AddPluginsForm(request)
        self.assertEqual(PluginVariants.objects.count(), 0)

    def test_forms_not_valid(self):
        fake_self = self.FakeSelf()
        plugin = Plugins.objects.create(name="Some")
        variant = PluginVariants.objects.create(instance=plugin)
        AddPluginsForm.forms_not_valid(fake_self, variant)
        self.assertEqual(fake_self.errors, [ADD_PLUGIN_ERROR_FILE])
        self.assertEqual(PluginVariants.objects.count(), 0)

    def test_handle_data_do_not_take_empty_dict(self):
        with StringIO("""{}""") as file:
            request = self.FakeRequest()
            request.FILES = {"plugin_file": file}
            request.POST.update({"plugin_name": "test 01"})
            form = AddPluginsForm(request)
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors, [ADD_PLUGIN_ERROR_FILE])

    def test_plugin_data_have_correct_structure(self):
        with StringIO("""{'test': 1}""") as file:
            request = self.FakeRequest()
            request.FILES = {"plugin_file": file}
            request.POST.update({"plugin_name": "test 02"})
            form = AddPluginsForm(request)
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors, [ADD_PLUGIN_ERROR_FILE])


class PluginVariantsFormTest(TestCase):

    def setUp(self):
        plugin = Plugins.objects.create(name="test 01")

        self.data = QueryDict("", mutable=True)
        corrected_dict = copy.deepcopy(PLUGIN_TEST_DICT)
        corrected_dict.pop("isEsl")
        self.data.update({
            "version": "0.1",
            "language": "Polish",
            "is_esl": False,
            "plugin_data": corrected_dict,
            "instance": plugin,
        })

    def count_plugins_or_variants(self, amount, name, plugins=True):
        instance, created = Plugins.objects.get_or_create(name=name)
        self.data.update({"instance": instance})
        variant = PluginVariantsForm(data=self.data)
        if not variant.is_valid():
            print(variant.errors)
        variant.save()
        if plugins:
            self.assertEqual(len(Plugins.objects.all()), amount)
        else:
            self.assertEqual(len(Plugins.objects.all()), 1)
            self.assertEqual(len(PluginVariants.objects.filter(instance=instance)), amount)

    def test_unique_validation(self):
        form = PluginVariantsForm(data=self.data)
        self.assertTrue(form.is_valid())
        form.save()
        other_form = PluginVariantsForm(data=self.data)
        self.assertFalse(other_form.is_valid())

        plugin = Plugins.objects.create(name="test 02", usable_name="test")
        self.data.update({"instance": plugin})
        another_form = PluginVariantsForm(data=self.data)
        self.assertTrue(another_form.is_valid())

    def test_form_create_new_plugin_only_if_there_is_new_name(self):

        self.count_plugins_or_variants(1, "test 01", plugins=True)

        self.count_plugins_or_variants(2, "test 02", plugins=True)

        self.data.update({"version": "0.2"})

        self.count_plugins_or_variants(2, "test 02", plugins=True)

    def test_form_create_plugins_variants_for_each_version(self):

        self.count_plugins_or_variants(1, "test 01", plugins=False)

        self.data.update({"version": "0.2"})

        self.count_plugins_or_variants(2, "test 01", plugins=False)

        self.data.update({"language": "English"})

        self.count_plugins_or_variants(3, "test 01", plugins=False)

    def test_plugin_version_is_stripped_from_most_special_signs(self):
        self.data.update({"version": "a!@#$%^&*()_-=+;:\"\',<>./?`~\\|"})
        form = PluginVariantsForm(data=self.data)
        self.assertTrue(form.is_valid())
        form.save()
        plugin_variant = PluginVariants.objects.first()
        self.assertEqual(plugin_variant.version, "a_-;:,.")


class EscapeHtmlForFormsTest(TestCase):
    def test_escape(self):
        self.assertEqual("&amp;test", escape_html_for_forms("&test"))
        self.assertEqual("&gt;some", escape_html_for_forms(">some"))

    def test_escape_can_handle_wrong_data(self):
        cases = [None, [None], [{None}]]
        for case in cases:
            with self.assertRaises(ValidationError, msg=f"Fail on {case}"):
                escape_html_for_forms(case)


class GetDataTest(TestCase):
    def test_return_data_from_dict(self):
        item = {"test": "a"}
        result = get_data(item, "test")
        self.assertEqual("a", result)

    def test_result_is_html_escaped(self):
        item = {"test": "&yes<>"}
        result = get_data(item, "test")
        self.assertEqual("&amp;yes&lt;&gt;", result)

    def test_data_are_stringify(self):
        item = {"test": 1}
        result = get_data(item, "test")
        self.assertEqual("1", result)

    def test_raise_validation_error_on_attribute_error(self):
        with self.assertRaises(ValidationError):
            get_data(None, "")


class GetCleanedDataTest(TestCase):
    def setUp(self):
        self.cleaned_data = {"field": ["Some data!"]}

    def test_return_data(self):
        actual = get_cleaned_data(self, "field")
        self.assertEqual(actual, ["Some data!"])

    def test_if_none_return_empty_list(self):
        self.cleaned_data = {"field": None}
        actual = get_cleaned_data(self, "field")
        self.assertEqual(actual, [])

    def test_if_not_list_raise_validation_error(self):
        self.cleaned_data = {"field": 1}
        with self.assertRaises(ValidationError):
            get_cleaned_data(self, "field")


class ItemsBaseTest(TestCase):
    def setUp(self):
        plugin = Plugins.objects.create(name="test")
        self.variant = PluginVariants.objects.create(instance=plugin, version="1", language="any", is_esl=False)
        self.all_data = copy.deepcopy(PLUGIN_TEST_DICT)


class BaseItemsFormTest(ItemsBaseTest):
    def setUp(self):
        super().setUp()
        self.data = self.all_data.get("WEAP")

    def test_forms_are_subclass_of_base_items_form(self):
        forms = [WeaponsForm, ArmorsForm, AmmoForm, AlchemyForm, BooksForm, IngredientsForm, MiscellaneousForm,
                 KeysForm, ScrollsForm, SoulsGemsForm]
        for form in forms:
            self.assertTrue(issubclass(form, BaseItemsForm), msg=f"Fail on: {form}")

    def test_pass_data_to_model(self):
        form = WeaponsForm({"items": self.data, "variant": self.variant})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Weapons.objects.count(), 1)

    def test_data_are_stringify(self):
        form = WeaponsForm({"items": self.data, "variant": self.variant})
        form.save()
        self.assertEqual(Weapons.objects.first().items[0].get("weight"), "17")

    def test_data_are_html_escaped(self):
        self.data[0].update({"fullName": "&html<escaped>"})
        form = WeaponsForm({"items": self.data, "variant": self.variant})
        form.save()
        self.assertEqual(Weapons.objects.first().items[0].get("name"), "&amp;html&lt;escaped&gt;")

    def test_form_can_take_empty_list(self):
        form = WeaponsForm({"weapons": [], "variant": self.variant})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual([], Weapons.objects.first().items)


class WeaponsFormTest(TestCase):
    def test_get_item_data(self):
        expected = {"name": "", "editor_id": "", "form_id": "", "weight": "", "value": "", "damage": "",
                    "description": "", "type": ""}
        actual = WeaponsForm.get_item_data({"fullName": "", "editorId": "", "formId": "", "Weight": "", "Damage": "",
                                            "Type": "", "Description": "", "Value": ""})
        self.assertEqual(expected, actual)


class ArmorsFormTest(TestCase):
    def test_get_item_data(self):
        expected = {"name": "", "editor_id": "", "form_id": "", "weight": "", "value": "", "armor_rating": "",
                    "description": "", "armor_type": ""}
        actual = ArmorsForm.get_item_data({"fullName": "", "editorId": "", "formId": "", "Weight": "", "Value": "",
                                           "Description": "", "Armor type": "", "Armor rating": ""})
        self.assertEqual(expected, actual)


class BooksFormTest(TestCase):
    def test_get_item_data(self):
        expected = {"name": "", "editor_id": "", "form_id": "", "weight": "", "value": ""}
        actual = BooksForm.get_item_data({"fullName": "", "editorId": "", "formId": "", "Weight": "", "Value": ""})
        self.assertEqual(expected, actual)


class IngredientsFormTest(TestCase):
    def test_get_item_data(self):
        expected = {"name": "", "editor_id": "", "form_id": "", "weight": "", "value": "", "effects": ""}
        actual = IngredientsForm.get_item_data({"fullName": "", "editorId": "", "formId": "", "Weight": "",
                                                "Value": "", "Effects": ""})
        self.assertEqual(expected, actual)


class AlchemyFormTest(TestCase):
    def test_get_item_data(self):
        expected = {"name": "", "editor_id": "", "form_id": "", "weight": "", "value": "", "effects": ""}
        actual = AlchemyForm.get_item_data({"fullName": "", "editorId": "", "formId": "", "Weight": "",
                                            "Value": "", "Effects": ""})
        self.assertEqual(expected, actual)


class MiscellaneousFormTest(TestCase):
    def test_get_item_data(self):
        expected = {"name": "", "editor_id": "", "form_id": "", "weight": "", "value": ""}
        actual = MiscellaneousForm.get_item_data({"fullName": "", "editorId": "", "formId": "", "Weight": "",
                                                  "Value": ""})
        self.assertEqual(expected, actual)


class AmmoFormTest(TestCase):
    def test_get_item_data(self):
        expected = {"name": "", "editor_id": "", "form_id": "", "weight": "", "value": "", "damage": ""}
        actual = AmmoForm.get_item_data({"fullName": "", "editorId": "", "formId": "", "Weight": "",
                                         "Value": "", "Damage": ""})
        self.assertEqual(expected, actual)


class ScrollsFormTest(TestCase):
    def test_get_item_data(self):
        expected = {"name": "", "editor_id": "", "form_id": "", "weight": "", "value": "", "effects": ""}
        actual = ScrollsForm.get_item_data({"fullName": "", "editorId": "", "formId": "", "Weight": "",
                                            "Value": "", "Effects": ""})
        self.assertEqual(expected, actual)


class SoulGemsFormTest(TestCase):
    def test_get_item_data(self):
        expected = {"name": "", "editor_id": "", "form_id": "", "weight": "", "value": ""}
        actual = SoulsGemsForm.get_item_data({"fullName": "", "editorId": "", "formId": "", "Weight": "", "Value": ""})
        self.assertEqual(expected, actual)


class KeysFormTest(TestCase):
    def test_get_item_data(self):
        expected = {"name": "", "editor_id": "", "form_id": "", "weight": "", "value": ""}
        actual = KeysForm.get_item_data({"fullName": "", "editorId": "", "formId": "", "Weight": "", "Value": ""})
        self.assertEqual(expected, actual)


class PerksFormTest(ItemsBaseTest):
    def setUp(self):
        super().setUp()
        self.data = self.all_data.get("PERK")

    def test_pass_data_to_model_data_are_stringify_and_html_escape(self):
        form = PerksForm({"perks": self.data, "variant": self.variant})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Perks.objects.count(), 1)
        self.assertEqual(Perks.objects.first().perks[0].get("name"), "Dopasowane blachy")
        self.assertEqual(Perks.objects.first().perks[0].get("editor_id"), "DBWellFitted")
        self.assertEqual(Perks.objects.first().perks[0].get("form_id"), "01711C")
        self.assertEqual(Perks.objects.first().perks[0].get("description"),
                         "Premia +25 do pancerza, jeśli nosisz całą zbroję mroku.")

    def test_form_can_take_empty_list(self):
        form = PerksForm({"perks": [], "variant": self.variant})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual([], Perks.objects.first().perks)


class WordsOfPowerTest(ItemsBaseTest):
    def setUp(self):
        super().setUp()
        self.data = self.all_data.get("WOOP")

    def test_pass_data_to_model_data_are_stringify_and_html_escape(self):
        form = WordsOfPowerForm({"words": self.data, "variant": self.variant})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(WordsOfPower.objects.count(), 1)
        self.assertEqual(WordsOfPower.objects.first().words[0].get("word"), "Nus")
        self.assertEqual(WordsOfPower.objects.first().words[0].get("editor_id"), "WordNus")
        self.assertEqual(WordsOfPower.objects.first().words[0].get("form_id"), "0602A5")
        self.assertEqual(WordsOfPower.objects.first().words[0].get("translation"), "Posąg")

    def test_form_can_take_empty_list(self):
        form = WordsOfPowerForm({"words": [], "variant": self.variant})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual([], WordsOfPower.objects.first().words)


class SpellsFormTest(ItemsBaseTest):
    def setUp(self):
        super().setUp()
        self.data = self.all_data.get("SPEL")
        self.sorted_spells = {"alteration": [self.data[0]], "conjuration": [self.data[2]],
                              "destruction": [self.data[1]], "illusion": [self.data[3]], "restoration": [self.data[4]],
                              "other": [self.data[5]]}
        self.maxDiff = None

    def test_sort_post(self):
        actual = SpellsForm.sort_spells(self.data)
        self.assertDictEqual(actual, self.sorted_spells)

    def test_assign_spells_forms(self):
        actual = SpellsForm.assign_forms(self.sorted_spells, self.variant)
        expected = [AlterationSpellsForm, ConjurationSpellsForm, DestructionSpellsForm, IllusionSpellsForm,
                    RestorationSpellsForm, OtherSpellsForm]
        for index in range(6):
            self.assertIsInstance(actual[index], expected[index])

    def test_can_validate_correct_data(self):
        form = SpellsForm({"spells": self.data, "variant": self.variant})
        self.assertTrue(form.is_valid())

    def test_can_validate_incorrect_data(self):
        form = SpellsForm({})
        self.assertFalse(form.is_valid())

    def test_form_can_take_none(self):
        form = SpellsForm({"spells": None, "variant": self.variant})
        self.assertTrue(form.is_valid())
        form.save()

    def test_can_save(self):
        form = SpellsForm({"spells": self.data, "variant": self.variant})
        self.assertTrue(form.is_valid())
        models = [AlterationSpells, ConjurationSpells, DestructionSpells,
                  RestorationSpells, IllusionSpells, OtherSpells]
        self.assertEqual(0, sum(model.objects.count() for model in models))
        form.save()
        self.assertEqual(6, sum(model.objects.count() for model in models))


class BaseSpellsFormTest(ItemsBaseTest):
    def setUp(self):
        super().setUp()

    def test_forms_are_subclass_of_base_spell_form(self):
        forms = [AlterationSpellsForm, ConjurationSpellsForm, DestructionSpellsForm,
                 IllusionSpellsForm, RestorationSpellsForm, OtherSpellsForm]
        for form in forms:
            self.assertTrue(issubclass(form, BaseSpellForm), msg=f"Fail on {form}")

    def test_pass_data_to_model_data_are_stringify_and_html_escape(self):
        data = self.all_data.get("SPEL")[0]
        form = AlterationSpellsForm({"spells": [data], "variant": self.variant})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(AlterationSpells.objects.count(), 1)
        self.assertEqual(AlterationSpells.objects.first().spells[0].get("name"), "Alternation Spell")
        self.assertEqual(AlterationSpells.objects.first().spells[0].get("editor_id"), "DragonPriest")
        self.assertEqual(AlterationSpells.objects.first().spells[0].get("form_id"), "000001")
        self.assertEqual(AlterationSpells.objects.first().spells[0].get("effects"), "obrażeń od ognia na sekundę.")
        self.assertEqual(AlterationSpells.objects.first().spells[0].get("mastery"), "Expert")

    def test_form_can_take_empty_list(self):
        form = AlterationSpellsForm({"spells": [], "variant": self.variant})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual([], AlterationSpells.objects.first().spells)