from django.test import TestCase
from unittest.mock import patch
from smtplib import SMTPException


class MainPageTest(TestCase):

    def use_template(self, url, template):
        response = self.client.get(url)
        self.assertTemplateUsed(response, "main_page/" + template)

    def test_use_template(self):
        self.use_template("/", "home.html")
        self.use_template("/about_me", "about_me.html")
        self.use_template("/contact", "contact.html")


class ContactTest(TestCase):
    base_url = "/contact"

    @patch("main_page.views.send_mail")
    def test_can_send_message(self, mock_send_email):
        post = {"subject": "Test", "email": "test@test.com", "message": "Message"}
        self.client.post(self.base_url, post)
        mock_send_email.assert_called_once()
        mock_send_email.assert_called_with("Test", "Message", "test@test.com", ['foris.dev@gmail.com'])

        response = self.client.get(self.base_url)
        self.assertEqual(response.context["messages"], ["Message was sent!"])

    def test_redirect_after_post(self):
        post = {"subject": "Test", "email": "test@test.com", "message": "Message"}
        response = self.client.post(self.base_url, post)
        self.assertRedirects(response, self.base_url)

    @patch("main_page.views.send_mail")
    def test_can_handle_sending_error(self, mock_send_email):
        def raise_error(*args):
            raise SMTPException()
        mock_send_email.side_effect = raise_error
        post = {"subject": "Test", "email": "test@test.com", "message": "Message"}
        self.client.post(self.base_url, post)

        response = self.client.get(self.base_url)
        self.assertEqual(response.context["messages"], ["Something went wrong! "
                                                        "\nPlease try a different method of contact."])
