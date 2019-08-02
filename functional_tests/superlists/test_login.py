from selenium.webdriver.common.keys import Keys
import re

from functional_tests.base import (
    TEST_EMAIL, FOR_TEST_EMAIL
)
from .superlist_base import FunctionalTest

SUBJECT = "Your login link for Superlists."


class SuperlistLoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter het email address, so she does
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_name("email").send_keys(TEST_EMAIL)
        self.driver.find_element_by_name("email").send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            "Check your email",
            self.driver.find_element_by_tag_name("body").text
        ))

        # She check her email and finds a message
        body = self.wait_for_email(TEST_EMAIL, SUBJECT, FOR_TEST_EMAIL)

        # It has a utl link in it
        self.assertIn("Use this link to log in", body)
        url_search = re.search(r"http://.+/.+$", body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url[:-5], url)

        # She clicks it
        self.driver.get(url)

        # She is logged in!
        self.wait_to_be_logged_in(TEST_EMAIL)

        # Now she logs out
        self.driver.find_element_by_link_text("Log out").click()

        # She is logged out
        self.wait_to_be_logged_out(TEST_EMAIL)
