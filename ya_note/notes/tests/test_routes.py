from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from http import HTTPStatus

from notes.models import Note


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(username='Bob')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.note = Note.objects.create(
            title='test 1',
            text='test t1',
            slug='test-1',
            author=cls.user
        )
        cls.another_user = get_user_model().objects.create(username='David')
        cls.alien_client = Client()
        cls.alien_client.force_login(cls.another_user)

    def test_homepage_for_anonymous(self):
        response = self.client.get(reverse('notes:home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_pages_for_auth_user(self):
        urls = ('notes:list', 'notes:success', 'notes:add',)
        for url in urls:
            response = self.auth_client.get(reverse(url))
            with self.subTest(f'url: {url}'):
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_add_edit_delete_only_author(self):
        urls = (
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
        )
        client_status = (
            (self.auth_client, HTTPStatus.OK),
            (self.alien_client, HTTPStatus.NOT_FOUND),
            (self.client, HTTPStatus.FOUND),
        )
        for path, arg in urls:
            for client, status in client_status:
                url = reverse(path, args=arg)
                response = client.get(url)
                with self.subTest(f'client: {client}, status: {status}'):
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous(self):
        urls = (
            ('notes:list', None),
            ('notes:success', None),
            ('notes:add', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
        )
        url_login = reverse('users:login')

        for path, arg in urls:
            url = reverse(path, args=arg)
            response = self.client.get(url)
            redirect_url = f'{url_login}?next={url}'
            with self.subTest(f'path: {path}, arg: {arg}'):
                self.assertRedirects(response, redirect_url)

    def test_availability_pages_auth_for_all(self):
        urls = (
            'users:login',
            'users:logout',
            'users:signup',
        )
        clients = (self.client, self.auth_client)
        for url in urls:
            for client in clients:
                response = client.get(reverse(url))
                with self.subTest(f'client: {client}, url: {url}'):
                    self.assertEqual(response.status_code, HTTPStatus.OK)
