class BaseChosen:
    def __init__(self, request):
        self.request = request
        self._key = None

    def set(self, value):
        self.request.session.update({self._key: value})

    def get(self):
        return self.request.session.get(self._key, {})


class ChosenItems(BaseChosen):
    def __init__(self, *args):
        super().__init__(*args)
        self._key = "chosen_items"


class ChosenSpells(BaseChosen):
    def __init__(self, *args):
        super().__init__(*args)
        self._key = "chosen_spells"


class ChosenOther(BaseChosen):
    def __init__(self, *args):
        super().__init__(*args)
        self._key = "chosen_other"