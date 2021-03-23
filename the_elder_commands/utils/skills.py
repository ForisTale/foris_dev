from the_elder_commands.utils.defauld_skills_race_update import default_skills_race_update


class Skills:
    def __init__(self, request):
        self.request = request
        self._race_key = "race"
        self._default_race = "nord"
        self._skills_key = "skills"
        self._desired_level_key = "desired_level"
        self._multiplier_key = "multiplier"
        self._fill_skills_key = "fill_skills"

    def save_skills(self, skills):
        self.request.session.update({self._skills_key: skills})

    def save_desired_level(self, desired_level):
        self.request.session.update({self._desired_level_key: desired_level})

    def save_multiplier(self, multiplier):
        self.request.session.update({self._multiplier_key: multiplier})

    def save_race(self, race):
        self.request.session.update({self._race_key: race})

    def save_fill_skills(self, value):
        self.request.session.update({self._fill_skills_key: value})

    def get_race(self):
        return self.request.session.get(self._race_key, self._default_race)

    def get_skills(self):
        return self.request.session.get(self._skills_key, default_skills_race_update(self._default_race))

    def get_desired_level(self):
        return self.request.session.get(self._desired_level_key, 1)

    def get_multiplier(self):
        return self.request.session.get(self._multiplier_key, 1.5)

    def get_fill_skills(self):
        return self.request.session.get(self._fill_skills_key)