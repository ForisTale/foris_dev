from selenium.webdriver.common.keys import Keys
from functional_tests import base
from functional_tests.base import wait

from django.core import mail
from django.conf import settings

from functional_tests.superlists.server_tools import create_session_on_server
from functional_tests.superlists.management.commands.create_session import create_pre_authenticated_session

import time
import poplib


class FunctionalTest(base.FunctionalTest):
    def setUp(self):
        super().setUp()
        self.live_server_url = self.live_server_url + "/lists"

    def get_item_input_box(self):
        return self.driver.find_element_by_id("id_text")

    def add_list_item(self, item_text):
        num_rows = len(self.driver.find_elements_by_css_selector("#id_list_table tr"))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f"{item_number}: {item_text}")

    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.driver.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_to_be_logged_in(self, email):
        self.driver.find_element_by_link_text("Log out")
        navbar = self.driver.find_element_by_css_selector(".navbar")
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.driver.find_element_by_name("email")
        navbar = self.driver.find_element_by_css_selector(".navbar")
        self.assertNotIn(email, navbar.text)

    def wait_for_email(self, test_email, subject, for_test_email):

        if not self.staging_server:
            return self.wait_for_mock_email_body(test_email, subject)

        start = time.time()
        while time.time() - start < 60:
            email_id = None
            inbox = poplib.POP3_SSL("pop.mail.yahoo.com")
            try:
                inbox.user(test_email)
                inbox.pass_(for_test_email)
                # get 10 newest messages
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print("getting msg", i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode("utf-8") for l in lines]
                    if f"Subject: {subject}" in lines:
                        email_id = i
                        body = "\n".join(lines)
                        return body
                time.sleep(1)
            finally:
                if email_id:
                    inbox.dele(email_id)
                inbox.quit()

    @wait
    def wait_for_mock_email_body(self, test_email, subject):
        email = mail.outbox[0]
        self.assertIn(test_email, email.to)
        self.assertEqual(email.subject, subject)
        return email.body

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)

        else:
            session_key = create_pre_authenticated_session(email)

        # to set a cookie we need to first visit the domain.
        # 404 pages load the quickest!
        self.driver.get(self.live_server_url + "/404_no_such_url/")
        self.driver.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

