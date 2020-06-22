import copy

from django.http import QueryDict
from django.test import TestCase

from the_elder_commands.forms.validate_skills import ValidateSkills, SkillsValidationError
from the_elder_commands.inventory import DEFAULT_SKILL_POST, SKILLS_ERROR_DESIRED_LEVEL, \
    SKILLS_ERROR_DESIRED_LEVEL_RANGE, SKILLS_ERROR_MULTIPLIER, DEFAULT_SKILLS, SKILLS_ERROR_NEW_VALUE_BIGGER, \
    SKILLS_ERROR_BASE_SKILL, SKILLS_ERROR_DESIRED_SKILL


class ValidateSkillsTest(TestCase):

    class FakeRequest:
        def __init__(self):
            self.POST = QueryDict("", mutable=True)
            self.POST.update(DEFAULT_SKILL_POST)
            self.POST.update({
                "desired_level": "1",
                "priority_multiplier": "1.5",
                "illusion_base": "15",
                "illusion_new": "",
                "sneak_base": "15",
                "sneak_new": "25",
                "sneak_multiplier": "on",
                "fill_skills": "true"
            })
            self.session = {}

    class FakeValidateSkillsSelf:
        def __init__(self, request):
            self.request = request
            self.errors = []

    def setUp(self):
        super().setUp()
        self.maxDiff = None

    def test_is_valid(self):
        request = self.FakeRequest()
        form = ValidateSkills(request)
        self.assertTrue(form.is_valid())
        form.errors.append("Error!")
        self.assertFalse(form.is_valid())

    def test_desired_level_need_to_be_integer(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        cases = {"1": 1, "a": None, "1.2": None, "": None}
        for case, expected in cases.items():
            request.POST.update({"desired_level": case})
            value = ValidateSkills._desired_level_validation(fake_self)
            self.assertEqual(value, expected)

    def test_wrong_desired_level_give_correct_error(self):
        request = self.FakeRequest()
        request.POST.update({"desired_level": "a"})
        fake_self = self.FakeValidateSkillsSelf(request)
        ValidateSkills._desired_level_validation(fake_self)
        self.assertEqual(fake_self.errors, [SKILLS_ERROR_DESIRED_LEVEL])

    def test_desired_level_need_to_be_between_1_and_81(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        cases = {"1": 1, "81": 81, "82": None, "0": None, "-1": None}
        for case, expected in cases.items():
            request.POST.update({"desired_level": case})
            actual = ValidateSkills._desired_level_validation(fake_self)
            self.assertEqual(actual, expected, msg=f"Fail on {case}")

    def test_desired_level_range_give_correct_error(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        request.POST.update({"desired_level": "0"})
        ValidateSkills._desired_level_validation(fake_self)
        self.assertEqual(fake_self.errors, [SKILLS_ERROR_DESIRED_LEVEL_RANGE])

    def test_priority_multiplier_is_float(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        cases = {"1": 1, "a": None, "1.2": 1.2, "": None}
        for case, expected in cases.items():
            request.POST.update({"priority_multiplier": case})
            value = ValidateSkills._priority_multiplier_validation(fake_self)
            self.assertEqual(value, expected)

    def test_wrong_multiplier_give_correct_error(self):
        request = self.FakeRequest()
        request.POST.update({"priority_multiplier": "a"})
        fake_self = self.FakeValidateSkillsSelf(request)
        ValidateSkills._priority_multiplier_validation(fake_self)
        self.assertEqual(fake_self.errors, [SKILLS_ERROR_MULTIPLIER])

    def test_skills(self):
        request = self.FakeRequest()
        form = ValidateSkills(request)
        self.assertTrue(form.is_valid())
        skills = copy.deepcopy(DEFAULT_SKILLS)
        skills["Stealth"]["sneak"].update({"desired_value": 25, "multiplier": True})
        self.assertDictEqual(skills["Stealth"]["sneak"], form.skills["Stealth"]["sneak"])

    def test_desired_need_to_be_bigger(self):
        request = self.FakeRequest()
        request.POST.update({"sneak_base": "30"})
        form = ValidateSkills(request)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, [SKILLS_ERROR_NEW_VALUE_BIGGER.format(skill="Sneak")])

    def test_skills_have_bottom_and_upper_limit(self):
        cases = {"14": False, "15": True, "100": True, "101": False}
        for case, result in cases.items():
            request = self.FakeRequest()
            request.POST.update({"illusion_base": case})
            form = ValidateSkills(request)
            self.assertEqual(form.is_valid(), result, msg=f"Fail on {case}")
        for case, result in cases.items():
            request = self.FakeRequest()
            request.POST.update({"illusion_new": case})
            form = ValidateSkills(request)
            self.assertEqual(form.is_valid(), result, msg=f"Fail on {case}")

    def test_new_value_is_bigger(self):
        self.assertTrue(ValidateSkills.is_new_skill_bigger(1, 2))
        self.assertTrue(ValidateSkills.is_new_skill_bigger(2, 2))
        self.assertTrue(ValidateSkills.is_new_skill_bigger(1, ""))
        self.assertFalse(ValidateSkills.is_new_skill_bigger(2, 1))

    def test_form_has_own_copy_of_skills(self):
        request = self.FakeRequest()
        form = ValidateSkills(request)
        skills = DEFAULT_SKILLS

        self.assertNotEqual(form.skills, skills)

    def test_get_default_skill(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        actual = ValidateSkills._get_default_skill(self=fake_self, skill="sneak", skill_name="Sneak")
        self.assertEqual(actual, 15)

    def test_get_desired_skill(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        actual = ValidateSkills._get_desired_skill(self=fake_self, skill="sneak", skill_name="Sneak")
        self.assertEqual(actual, 25)

    def test_get_default_skill_validate_skill(self):
        request = self.FakeRequest()
        cases = {"15": True, "a": False, "": False, "1.5": False}
        for case, result in cases.items():
            request.POST.update({"sneak_base": case})
            fake_self = self.FakeValidateSkillsSelf(request)
            value = ValidateSkills._get_default_skill(self=fake_self, skill="sneak", skill_name="Sneak")
            self.assertEqual(ValidateSkills.is_valid(fake_self), result, msg=f"Fail on {case}")
            if not result:
                self.assertEqual(fake_self.errors, [SKILLS_ERROR_BASE_SKILL.format(skill="Sneak")])
            else:
                self.assertEqual(fake_self.errors, [])
                self.assertEqual(int(case), value)

    def test_get_desired_skill_validate_skill(self):
        request = self.FakeRequest()
        cases = {"15": True, "a": False, "": True, "1.5": False}
        for case, result in cases.items():
            request.POST.update({"sneak_new": case})
            fake_self = self.FakeValidateSkillsSelf(request)
            value = ValidateSkills._get_desired_skill(self=fake_self, skill="sneak", skill_name="Sneak")
            self.assertEqual(ValidateSkills.is_valid(fake_self), result, msg=f"Fail case {case}")
            if not result:
                self.assertEqual(fake_self.errors,
                                 [SKILLS_ERROR_DESIRED_SKILL.format(skill="Sneak")])
            else:
                self.assertEqual(fake_self.errors, [])
                self.assertEqual(case, str(value))

    def test_get_multiplier_skill(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        self.assertTrue(ValidateSkills._get_multiplier(self=fake_self, skill="sneak"))
        self.assertFalse(ValidateSkills._get_multiplier(self=fake_self, skill="illusion"))

    def test_get_fill_skills(self):
        request = self.FakeRequest()
        fake_self = self.FakeValidateSkillsSelf(request)
        self.assertTrue(ValidateSkills._get_fill_skills(fake_self))

    def test_get_fill_skills_is_false_by_default(self):
        request = self.FakeRequest()
        request.POST.pop("fill_skills")
        fake_self = self.FakeValidateSkillsSelf(request)
        self.assertFalse(ValidateSkills._get_fill_skills(fake_self))

    def test_can_save(self):
        request = self.FakeRequest()
        form = ValidateSkills(request)
        form.save()
        self.assertDictEqual(
            request.session,
            {"skills": form.skills, "desired_level": 1, "multiplier": 1.5, "fill_skills": "true"}
        )

    def test_save_only_if_valid(self):
        request = self.FakeRequest()
        form = ValidateSkills(request)
        form.errors.append("Error!")
        with self.assertRaises(SkillsValidationError):
            form.save()