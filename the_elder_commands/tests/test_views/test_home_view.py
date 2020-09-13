from django.test import TestCase


class TestHomePageView(TestCase):
    def test_use_template(self):
        response = self.client.get("/the_elder_commands/")
        self.assertTemplateUsed(response, "the_elder_commands/home.html")
