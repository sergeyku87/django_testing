from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


class TestContent(TestCase):
    COUNT_NOTES = 5

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(username='Bob')
        cls.author_client = Client()
        cls.author_client.force_login(cls.user)

        cls.alien_user = get_user_model().objects.create(username='David')
        cls.alien_client = Client()
        cls.alien_client.force_login(cls.alien_user)

        cls.notes_user = [
            Note.objects.create(
                title=f'title {index}',
                text=f'text {index}',
                slug=f'title-{user}-{index}',
                author=user,
            )
            for user in (cls.user, cls.alien_user)
            for index in range(cls.COUNT_NOTES)
        ]
        cls.data = {
            'title': 'probe title',
            'text': 'probe text',
            'slug': 'probe-title',
            'author': cls.user
        }

    def test_add_note_displayed_to_page_list(self):
        url = reverse('notes:list')
        resp = self.author_client.get(url)
        count_notes_befor = len(resp.context.get('object_list'))

        self.author_client.post(reverse('notes:add'), data=self.data)

        response = self.author_client.get(url)
        count_notes_after = len(response.context.get('object_list'))
        self.assertLess(count_notes_befor, count_notes_after)

    def test_separate_notes_for_different_users(self):
        clients = (
            (self.author_client, self.user),
            (self.alien_client, self.alien_user)
        )
        for client, user in clients:
            response = client.get(reverse('notes:list'))
            obj_list = response.context.get('object_list')
            for obj in obj_list:
                with self.subTest():
                    self.assertEqual(obj.author.username, user.username)

    def test_exist_form_for_pages_edit_delete(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.notes_user[0].slug,)),
        )
        for path, arg in urls:
            url = reverse(path, args=arg)
            response = self.author_client.get(url)
            with self.subTest():
                self.assertIn('form', response.context)
