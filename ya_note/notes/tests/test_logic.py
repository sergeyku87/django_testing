from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from pytils.translit import slugify

from notes.models import Note


class TestLogic(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(username='Bishop')
        cls.auth_user = Client()
        cls.auth_user.force_login(cls.user)
        cls.data = {
            'title': 'test1',
            'text': 'text1',
            'author': cls.user,
        }

    def test_add_for_users(self):
        users = (
            (self.client, 0),
            (self.auth_user, 1),
        )
        for client, count_note in users:
            url = reverse('notes:add')
            with self.subTest():
                client.post(url, data=self.data)
                self.assertEqual(Note.objects.count(), count_note)

    def test_unique_slug(self):
        slug_for_test = 'slug-test'
        with self.assertRaises(IntegrityError):
            for _ in range(2):
                Note.objects.create(
                    title='t-i-t-l-e',
                    text='t-e-x-t',
                    slug=slug_for_test,
                    author=self.user
                )

    def test_auto_fill_field_slug(self):
        Note.objects.create(
            title='not_slug',
            text='realy_not_slug',
            author=self.user
        )
        self.assertTrue(hasattr(Note.objects.last(), 'slug'))
        self.assertEqual(
            Note.objects.last().slug,
            slugify(Note.objects.last().title)
        )
