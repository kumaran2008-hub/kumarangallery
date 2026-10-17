from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage, FriendProfile, GalleryCategory


class GallerySiteTests(TestCase):
    def setUp(self):
        self.category = GalleryCategory(name="Summer", slug="summer", password="")
        self.category.set_password("secret-passphrase")
        self.category.save()

    def test_home_renders_categories_and_contact_form(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Summer")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_category_requires_password_and_unlocks_in_session(self):
        url = reverse("category_detail", kwargs={"slug": self.category.slug})

        response = self.client.get(url)
        self.assertContains(response, "Collection password")

        response = self.client.post(url, {"password": "wrong"})
        self.assertContains(response, "not correct")

        response = self.client.post(url, {"password": "secret-passphrase"})
        self.assertRedirects(response, url)
        response = self.client.get(url)
        self.assertContains(response, "Summer")
        self.assertNotContains(response, "Collection password")

    def test_contact_message_is_saved(self):
        response = self.client.post(reverse("home"), {
            "name": "A Friend",
            "email": "friend@example.com",
            "message": "Hello there!",
        })

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.get().email, "friend@example.com")

    def test_friend_list_and_story_page(self):
        friend = FriendProfile.objects.create(
            name="Alex",
            slug="alex",
            dp="friends/profiles/alex.jpg",
            story="A kind friend.",
        )

        response = self.client.get(reverse("friends_list"))
        self.assertContains(response, "Alex")

        response = self.client.get(
            reverse("friend_detail", kwargs={"slug": friend.slug})
        )
        self.assertContains(response, "A kind friend.")

    def test_category_password_is_stored_as_hash(self):
        self.category.refresh_from_db()

        self.assertNotEqual(self.category.password, "secret-passphrase")
        self.assertTrue(self.category.check_password("secret-passphrase"))
