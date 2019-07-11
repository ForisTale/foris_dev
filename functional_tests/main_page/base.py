from selenium import webdriver
from django.test import LiveServerTestCase


class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()
