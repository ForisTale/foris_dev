def click_javascript_button(self, button_class_name):
    button = self.wait_for(lambda: self.driver.find_element_by_class_name(button_class_name))
    self.driver.execute_script("arguments[0].click()", button)