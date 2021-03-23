def check_test_tag(self, tag_string):
    method = getattr(self, self._testMethodName)
    tags = getattr(method, "tags", {})
    if tag_string in tags:
        return True