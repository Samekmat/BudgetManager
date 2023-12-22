from http import HTTPStatus

from django.contrib.messages import Message
from django.contrib.messages.test import MessagesTestMixin
from django.test import Client, TestCase
from django.urls import reverse
from helper_models.factories import CategoryIncomeFactory, TagFactory
from helper_models.models import Category, Tag
from users.factories import UserFactory


class CategoryViewsTests(MessagesTestMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryIncomeFactory(user=self.user)
        self.client = Client()

        # Urls
        self.list_url = reverse("helper_models:categories")
        self.create_url = reverse("helper_models:category-create")
        self.update_url = reverse("helper_models:category-update", kwargs={"pk": self.category.id})

        # Log in user
        self.client.force_login(self.user)

    def test_category_list_view(self):
        # Access the category list view
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        # Check for categories in context
        self.assertIn("categories", response.context)
        categories = response.context["categories"]
        self.assertEqual(len(categories), 1)

        # Check with filter params
        filter_params = {"name": self.category.name, "type": self.category.type}
        response_filter = self.client.get(self.list_url, filter_params)
        self.assertEqual(response_filter.status_code, 200)
        self.assertIn("categories", response_filter.context)
        categories_filter = response_filter.context["categories"]
        self.assertEqual(len(categories_filter), 1)

    def test_category_create_view(self):
        category_data = {
            "name": self.category.name,
            "type": self.category.type,
            "description": self.category.description,
        }
        response = self.client.post(self.create_url, category_data)

        # Check redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)

        # Check if category exist in db
        self.assertTrue(Category.objects.filter(name=self.category.name).exists())

        # Check message
        self.assertMessages(response, [Message(level=25, message="Category created successfully.")])

    def test_category_update_view(self):
        updated_category_data = {
            "name": "New Category name",
            "type": self.category.type,
            "description": "New description",
        }

        # Post data
        response = self.client.post(self.update_url, updated_category_data)  # , follow=True)

        # Check redirect/response
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.list_url)

        # Check that the Category was updated in the database
        updated_category = Category.objects.get(id=self.category.id)
        self.assertEqual(updated_category.name, "New Category name")
        self.assertEqual(updated_category.type, self.category.type)
        self.assertEqual(updated_category.description, "New description")

        # Check message
        self.assertMessages(response, [Message(level=25, message="Category updated successfully.")])


class TagViewsTest(MessagesTestMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = Client()
        self.tag = TagFactory(user=self.user)

        # Urls
        self.list_url = reverse("helper_models:tags")
        self.create_url = reverse("helper_models:tag-create")
        self.update_url = reverse("helper_models:tag-update", kwargs={"pk": self.tag.id})

        # Log in user
        self.client.force_login(self.user)

    def test_tag_list_view(self):
        # Access the tag list view
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        # Check for tags in context
        self.assertIn("tags", response.context)
        tags = response.context["tags"]
        self.assertEqual(len(tags), 1)

        # Check with filter params
        filter_params = {
            "name": self.tag.name,
        }
        response_filter = self.client.get(self.list_url, filter_params)
        self.assertEqual(response_filter.status_code, 200)
        self.assertIn("tags", response_filter.context)
        categories_filter = response_filter.context["tags"]
        self.assertEqual(len(categories_filter), 1)

    def test_tag_create_view(self):
        tag_data = {"name": "new_tag", "user": self.user.id}
        response = self.client.post(self.create_url, tag_data)

        # Check redirect
        self.assertEqual(response.status_code, 302)

        # Check if tag exist in db
        self.assertTrue(Tag.objects.filter(name="new_tag").exists())

        # Check message
        self.assertMessages(response, [Message(level=25, message="Tag created successfully.")])

    def test_tag_update_view(self):
        updated_tag_data = {"name": "Updated name"}

        # Post the updated form data to the update view
        response = self.client.post(self.update_url, updated_tag_data)

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Check that the redirect URL is correct
        self.assertRedirects(response, self.list_url)

        # Check that the Income was updated in the database
        updated_tag = Tag.objects.get(id=self.tag.id)
        self.assertEqual(updated_tag.name, updated_tag_data["name"])

        # Check message
        self.assertMessages(response, [Message(level=25, message="Tag updated successfully.")])
