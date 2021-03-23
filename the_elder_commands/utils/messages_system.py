class MessagesSystem:
    def __init__(self, request):
        self.request = request
        self._items_key = "items_messages"
        self._plugins_key = "plugins_messages"
        self._skills_key = "skills_messages"
        self._spells_key = "spells_messages"
        self._other_key = "other_messages"
        self._contact_key = "contact_messages"

    def append_plugin(self, message):
        self._append_message(self._plugins_key, message)

    def append_item(self, message):
        self._append_message(self._items_key, message)

    def append_skills(self, message):
        self._append_message(self._skills_key, message)

    def append_spells(self, message):
        self._append_message(self._spells_key, message)

    def append_other(self, message):
        self._append_message(self._other_key, message)

    def append_contact(self, message):
        self._append_message(self._contact_key, message)

    def _append_message(self, key, message):
        if type(message) == list:
            try:
                self._append_message(key, message.pop(0))
                self._append_message(key, message)
            except IndexError:
                pass
        else:
            new_message = self.request.session.get(key, [])
            new_message.append(message)
            self.request.session.update({key: new_message})

    def pop_items(self):
        return self._pop_messages(self._items_key)

    def pop_plugins(self):
        return self._pop_messages(self._plugins_key)

    def pop_skills(self):
        return self._pop_messages(self._skills_key)

    def pop_spells(self):
        return self._pop_messages(self._spells_key)

    def pop_other(self):
        return self._pop_messages(self._other_key)

    def pop_contact(self):
        return self._pop_messages(self._contact_key)

    def _pop_messages(self, key):
        message = self.request.session.get(key, [])
        self.request.session.update({key: []})
        return message