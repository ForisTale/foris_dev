from django.test import TestCase
from django.http import JsonResponse
from the_elder_commands.inventory import PLUGIN_TEST_DICT
from the_elder_commands.utils_for_tests import populate_plugins_table
import json
import copy


class ItemsApiTest(TestCase):
    base_url = "/api/tec/items/{}/"

    def setUp(self):
        self.maxDiff = None
        populate_plugins_table()
        session = self.client.session
        session.update({"selected": [{
            "name": "test 01",
            "usable_name": "test_01",
            "version": "03",
            "language": "english",
            "load_order": "A5"
        }]})
        session.save()

    def test_get_return_json_200(self):

        response = self.client.get(self.base_url.format("WEAP"))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_api_return_json_with_correct_data(self):
        response = self.client.get(self.base_url.format("WEAP"))

        test_dict = copy.deepcopy(PLUGIN_TEST_DICT.get("WEAP"))
        for item in test_dict:
            item.update({"formId": f"A5{item.get('formId', '')}", "plugin_name": "test 01", "quantity": "",
                         "selected": False})

        actual = json.loads(response.content)
        self.assertEqual(actual, test_dict)
