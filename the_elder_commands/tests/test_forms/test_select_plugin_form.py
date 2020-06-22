from django.http import QueryDict
from django.test import TestCase

from the_elder_commands.forms.selected_plugin_form import SelectedPluginsForm
from the_elder_commands.inventory import INCORRECT_LOAD_ORDER
from the_elder_commands.models import Plugins


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