def select_plugin(self):
    session = self.client.session
    session.update({"selected": [{
            "name": "test 01",
            "usable_name": "test_01",
            "version": "03",
            "language": "english",
            "load_order": "A5",
            "is_esl": False,
        }]})
    session.save()