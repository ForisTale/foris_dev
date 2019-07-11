from .base import FunctionalTest


class BasicTest(FunctionalTest):

    def test_has_basic_functionality(self):
        # Foris visit his new website.
        self.driver.get(self.live_server_url)

        # On page title is its website name
        self.assertEqual(self.driver.title, "Foris.dev")

        # In navigation bar there is link to main site and about me page
        links = self.driver.find_elements_by_tag_name("a")
        links = [link.text for link in links]
        self.assertIn("Foris.dev", links)
        self.assertIn("About Me", links)

        # He click on about me
        self.driver.find_element_by_link_text("About Me").click()
        desired_location = self.live_server_url + "/about_me"
        self.assertEqual(desired_location, self.driver.current_url)

        # There is basic description about him
        description = self.driver.find_element_by_id("about_me").text
        self.assertNotEqual(description, "")

        # And sees links to his github, and other sites
        all_links = self.driver.find_elements_by_tag_name("li")
        all_links = [link.text for link in all_links]
        my_link = "My github."
        self.assertIn(my_link, all_links)

        # Satisfied he click on main site link and is back to main site.
        self.driver.find_element_by_link_text("Foris.dev").click()
        self.assertEqual(self.driver.current_url, self.live_server_url + "/")
