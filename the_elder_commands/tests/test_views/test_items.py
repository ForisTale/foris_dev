from django.test import TestCase


class ItemsViewTest(TestCase):

    def test_items_use_template(self):
        response = self.client.get("/the_elder_commands/items/")
        self.assertTemplateUsed(response, "the_elder_commands/items.html")
