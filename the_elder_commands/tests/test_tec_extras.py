from django.test import TestCase
from the_elder_commands.templatetags.tec_extras import get_chosen_amount


class GetChosenAmountTest(TestCase):

    def test_return_chosen_amount(self):

        class FakeService:
            chosen = {"A1": "1"}

        fake_item = {"formId": "A1"}
        actual = get_chosen_amount(FakeService, fake_item)
        self.assertEqual(actual, "1")

    def test_if_not_chosen_return_empty_string(self):
        class FakeService:
            chosen = {}

        fake_item = {"formId": "A1"}
        actual = get_chosen_amount(FakeService, fake_item)
        self.assertEqual(actual, "")
