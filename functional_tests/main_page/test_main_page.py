from functional_tests.base import FunctionalTest


class MainPageBasicTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        # Foris visit his new website.
        self.driver.get(self.live_server_url)

    def check_link_send_to_correct_url(self, link_text, url_ending):
        self.driver.find_element_by_link_text(link_text).click()
        current_url = self.driver.current_url
        desired_url = self.live_server_url + url_ending
        self.assertEqual(current_url, desired_url)

    def test_has_basic_functionality(self):
        # On page title is its website name
        self.assertEqual(self.driver.title, "Foris.dev")

        # In navigation bar there is link to main site and about me page
        links = self.driver.find_elements_by_tag_name("a")
        links = [link.text for link in links]
        self.assertIn("Foris.dev", links)
        self.assertIn("About Me", links)

        # He click on about me
        self.check_link_send_to_correct_url("About Me", "/about_me")

        # There is basic description about him
        description = self.driver.find_element_by_id("about_me").text
        self.assertNotEqual(description, "")

        # And sees links to his github, and other sites
        all_links = self.driver.find_elements_by_tag_name("li")
        all_links = [link.text for link in all_links]
        self.assertIn("GitHub", all_links)

        # Satisfied he click on main site link and is back to main site.
        self.driver.find_element_by_link_text("Foris.dev").click()
        self.assertEqual(self.driver.current_url, self.live_server_url + "/")

    def test_can_go_to_the_elder_commands_and_back(self):

        # He spotted new link to TEC, decided to visit it.
        self.check_link_send_to_correct_url("The Elder Commands", "/the_elder_commands/")

        # Everything looks ok so he come back to main site by link.
        self.check_link_send_to_correct_url("Foris.dev", "/")

    def test_contact_allow_to_send_email_to_administrator(self):
        # Foris want send message to page admin
        # so he click contact
        self.wait_for(lambda: self.driver.find_element_by_link_text("Contact").click())
        self.wait_for(lambda: self.assertEqual(self.driver.current_url, self.live_server_url + "/contact"))

        # there he sees contact form so he fill it
        self.wait_for(lambda: self.driver.find_element_by_name("email").send_keys("test@test.com"))
        self.driver.find_element_by_name("subject").send_keys("Subject")
        self.driver.find_element_by_name("message").send_keys("Message")

        # then send it
        self.driver.find_element_by_id("id_submit").click()

        # now he sees message that massage was send
        message = self.wait_for(lambda: self.driver.find_element_by_class_name("messages").text)
        self.assertIn("Message was sent!", message)
