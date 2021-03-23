class FakeRequest:
    def __init__(self, data):
        self.POST = data
        self.session = {}