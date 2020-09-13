from django.test import TestCase
from the_elder_commands.services import SkillsService
from the_elder_commands.inventory import DEFAULT_SKILL_POST, COMMANDS_SUCCESS_MESSAGE, SKILLS_ERROR_DESIRED_LEVEL
from the_elder_commands.utils import default_skills_race_update


class SkillsViewTest(TestCase):
    def setUp(self):
        self.base_url = "/the_elder_commands/skills/"
        self.maxDiff = None

    def test_tec_use_template(self):
        response = self.client.get(self.base_url)
        self.assertTemplateUsed(response, "the_elder_commands/skills.html")

    def test_race_post_is_saved_in_skills(self):
        self.client.post(self.base_url, data={"race": "ork"})
        session = self.client.session
        self.assertEqual(session.get("race"), "ork")

    def test_redirect_after_race_post(self):
        response = self.client.post(self.base_url, data={"race": "ork"})
        self.assertRedirects(response, self.base_url)

    def test_pass_service_to_template(self):
        response = self.client.get(self.base_url)
        self.assertIsInstance(response.context["service"], SkillsService)

    def test_change_race_reset_skills(self):
        post = DEFAULT_SKILL_POST
        post.update({"desired_level": 1, "priority_multiplier": 1.5, "fill_skills": "true"})
        self.client.post(self.base_url, data=post)
        self.client.post(self.base_url, data={"race": "ork"})
        response = self.client.get(self.base_url)
        actual = response.context["service"]
        expected = default_skills_race_update("ork")
        self.assertDictEqual(actual.skills, expected)
        self.assertEqual(actual.fill_skills, None)

    def test_skill_post_is_passed_to_form_and_saved(self):
        self.client.get(self.base_url)
        self.client.post(self.base_url, data={"race": "ork"})
        response = self.client.get(self.base_url)
        self.assertEqual(response.context["service"].race, "ork")

        post = DEFAULT_SKILL_POST
        post.update({"priority_multiplier": 2.5, "desired_level": "1", "fill_skills": "true"})
        self.client.post(self.base_url, data=post)
        response = self.client.get(self.base_url)
        actual = response.context["service"]
        self.assertEqual(actual.multiplier, 2.5)
        self.assertEqual(actual.fill_skills, "true")
        self.assertEqual(actual.skills["Combat"]["heavyarmor"]["default_value"], 15)

    def test_pass_success_message_after_skills_post(self):
        post = DEFAULT_SKILL_POST
        post.update({"desired_level": 1, "priority_multiplier": 1.5})
        self.client.post(self.base_url, post)
        response = self.client.get(self.base_url)
        self.assertEqual(response.context["messages"], [COMMANDS_SUCCESS_MESSAGE])

    def test_pass_error_after_wrong_post(self):
        post = DEFAULT_SKILL_POST
        post.update({"desired_level": "a", "priority_multiplier": 1.5})
        self.client.post(self.base_url, post)
        response = self.client.get(self.base_url)
        self.assertEqual(response.context["messages"], [SKILLS_ERROR_DESIRED_LEVEL])

    def test_redirect_after_failed_post(self):
        post = DEFAULT_SKILL_POST
        post.update({"desired_level": "a", "priority_multiplier": 1.5})
        response = self.client.post(self.base_url, post)
        self.assertRedirects(response, self.base_url)

    def test_pass_commands(self):
        post = DEFAULT_SKILL_POST
        post.update({"block_new": "25"})
        post.update({"desired_level": 1, "priority_multiplier": 1.5})
        self.client.post(self.base_url, post)
        self.client.get(self.base_url)
        session = self.client.session
        self.assertEqual(session.get("skills_commands"), ["player.advskill block 826"])
