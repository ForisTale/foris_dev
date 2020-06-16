from django.test import TestCase
from django.test.utils import tag
from the_elder_commands.utils_for_tests import check_test_tag, select_plugin, populate_plugins_table
from the_elder_commands.inventory import NO_PLUGIN_SELECTED_ERROR_MESSAGE


class SpellsViewTest(TestCase):

    def setUp(self):
        populate_plugins_table()

        if check_test_tag(self, "dont_select"):
            pass
        else:
            select_plugin(self)

        self.base_url = "/the_elder_commands/spells/"

    def test_view_use_template(self):
        response = self.client.get(self.base_url)
        self.assertTemplateUsed(response, "the_elder_commands/spells.html")

    @tag("dont_select")
    def test_redirect_when_plugin_not_selected(self):
        response = self.client.get(self.base_url)
        self.assertRedirects(response, "/the_elder_commands/plugins/")

    @tag("dont_select")
    def test_not_selected_give_error_message(self):
        self.client.get(self.base_url)
        session = self.client.session
        self.assertEqual(session.get("plugins_messages"), [NO_PLUGIN_SELECTED_ERROR_MESSAGE])
