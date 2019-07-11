from django.test import TestCase


class MainPageTest(TestCase):

    def use_template(self, url, template):
        response = self.client.get(url)
        self.assertTemplateUsed(response, "main_page/" + template)

    def test_use_template(self):
        self.use_template("/", "home.html")
        self.use_template("/about_me", "about_me.html")

