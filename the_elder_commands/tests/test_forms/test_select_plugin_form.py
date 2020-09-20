from django.http import QueryDict
from django.test import TestCase

from the_elder_commands.forms.selected_plugin_form import SelectedPluginsForm
from the_elder_commands.inventory import INCORRECT_LOAD_ORDER, NO_PLUGIN_SELECTED
from the_elder_commands.models import Plugins


class FakeRequest:
    def __init__(self, data):
        self.POST = data
        self.session = {}


class SelectPluginFormTest(TestCase):

    def setUp(self):

        self.data = QueryDict("", mutable=True)
        self.post = '[{{"name": "test_01", "variant": "0.1&english&", "load_order": "{load_order}"}}, ' \
                    '{{"name": "test_02", "variant": "0.2&english&esl", "load_order": "FE001"}}]'
        Plugins.objects.create(name="test 01", usable_name="test_01")
        Plugins.objects.create(name="test 02", usable_name="test_02")

    def validate_load_order_cases(self, cases):
        for case, result in cases.items():
            self.data["selected_plugins"] = self.post.format(load_order=case)
            form = SelectedPluginsForm(request=FakeRequest(self.data))
            self.assertEqual(form.is_valid(), result, msg=f"{case} {result} {form.errors}")
            if result is False:
                self.assertEqual(form.errors[0], INCORRECT_LOAD_ORDER)

    def test_validate_load_order_for_esp(self):
        cases = {"A1": True, "*s": False, "AA1": False, "": False, "3": False, "#": False, "FE001": False, "FE1": False}
        self.post = '[{{"name": "test_01", "variant": "0.1&english&", "load_order": "{load_order}"}}]'
        self.validate_load_order_cases(cases)

    def test_validate_load_order_for_esl(self):
        cases = {"A1": False, "*s": False, "AA1": False, "": False, "3": False, "#": False, "FE001": True, "FE1": False,
                 "AB001": False, "FF001": True}
        self.post = '[{{"name": "test_02", "variant": "0.2&english&esl", "load_order": "{load_order}"}}]'
        self.validate_load_order_cases(cases)

    def test_is_esl(self):

        self.data["selected_plugins"] = self.post.format(load_order="01")
        form = SelectedPluginsForm(FakeRequest(self.data))

        self.assertEqual(form.is_esl({"name": "test_01", "variant": "0.1&english&", "load_order": "01"}), False)
        self.assertEqual(form.is_esl({"name": "test_01", "variant": "0.1&english&esl", "load_order": "FE001"}), True)

    def test_form_process_data(self):

        self.data["selected_plugins"] = self.post.format(load_order="01")
        request = FakeRequest(self.data)

        SelectedPluginsForm(request=request)
        expected = [{
            "name": "test 01",
            "usable_name": "test_01",
            "version": "0.1",
            "language": "english",
            "load_order": "01",
            "is_esl": False,
        }]
        self.assertDictEqual(request.session.get("selected", [])[0], expected[0])
        self.assertEqual(request.session.get("selected")[1].get("is_esl"), True)

    def test_get_data(self):
        self.data["selected_plugins"] = self.post.format(load_order="01")
        actual = SelectedPluginsForm.get_data(FakeRequest(self.data))
        expected = [{"name": "test_01", "variant": "0.1&english&", "load_order": "01"},
                    {"name": "test_02", "variant": "0.2&english&esl", "load_order": "FE001"}]
        self.assertEqual(actual, expected)

    def test_empty_post_give_error(self):
        self.data["selected_plugins"] = '[]'
        form = SelectedPluginsForm(FakeRequest(self.data))

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, [NO_PLUGIN_SELECTED])
