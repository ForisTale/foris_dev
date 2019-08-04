from django.test import TestCase
from django.utils.html import escape
from lists.models import Item, List
from lists.forms import (
    EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm
)
from unittest.mock import patch, Mock
from django.http import HttpRequest
from lists.views import new_list
import unittest
from django.contrib.auth import get_user_model
from lists.views import USER_DONT_EXISTS_ERROR

User = get_user_model()


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get("/lists/")
        self.assertTemplateUsed(response, "lists/home.html")

    def test_home_page_uses_item_form(self):
        response = self.client.get("/lists/")
        self.assertIsInstance(response.context["form"], ItemForm)


class ListViewTest(TestCase):

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            f"/lists/{list_.id}/",
            data={"text": ""}
        )

    def test_uses_list_templates(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "lists/list.html")

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)

    def test_can_save_a_post_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new item for an existing list."}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list.")
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirect_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new item to an existing list."}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_render_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lists/list.html")

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertIsInstance(response.context["form"], ExistingListItemForm)
        self.assertContains(response, 'name="text"')


class NewListViewIntegratedTest(TestCase):

    def test_can_save_a_post_request(self):
        self.client.post("/lists/new", data={"text": "A new list item."})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item.")

    def test_for_invalid_input_doesnt_save_but_shows_error(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email="a@b.com")
        self.client.force_login(user)
        self.client.post("/lists/new", data={"text": "new item"})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


class MyListTest(TestCase):

    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email="a@b.com")
        response = self.client.get("/lists/users/a@b.com/")
        self.assertTemplateUsed(response, "lists/my_lists.html")

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email="wrong@owner.com")
        correct_user = User.objects.create(email="a@b.com")
        response = self.client.get("/lists/users/a@b.com/")
        self.assertEqual(response.context["owner"], correct_user)


@patch("lists.views.NewListForm")
class NewListViewUnitTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST["text"] = "new list item"
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        new_list(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch("lists.views.redirect")
    def test_redirect_to_form_returned_object_if_form_valid(
            self, mock_redirect, mockNewListForm
    ):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True

        response = new_list(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(str(mock_form.save.return_value))

    @patch("lists.views.render")
    def test_renders_home_template_with_form_if_form_invalid(
            self, mock_render, mock_NewListForm
    ):
        mock_form = mock_NewListForm.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, "lists/home.html", {"form": mock_form}
        )

    def test_does_not_save_if_form_invalid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        self.assertFalse(mock_form.save.called)


class SharedViewTest(TestCase):

    def test_can_add_user_to_list(self):
        shared = User.objects.create(email="a@b.com")
        list_ = List.objects.create()
        self.client.post(
            f"/lists/{list_.id}/share",
            data={"sharee": "a@b.com"}
        )

        self.assertIn(shared, list_.shared_with.all())

    def test_add_non_exist_user_is_not_save_and_return_error(self):
        list_ = List.objects.create()
        response = self.client.post(
            f"/lists/{list_.id}/share",
            data={"sharee": "non@exist.com"}
        )
        self.assertEqual(list_.shared_with.count(), 0)
        self.assertContains(response, escape(USER_DONT_EXISTS_ERROR))

    def test_redirect_after_POST(self):
        User.objects.create(email="a@b.com")
        list_ = List.objects.create()

        response = self.client.post(
            f"/lists/{list_.id}/share",
            data={"sharee": "a@b.com"}
        )

        self.assertRedirects(response, f"/lists/{list_.id}/")
