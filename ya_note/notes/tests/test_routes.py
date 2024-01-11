from http import HTTPStatus

from .fixtures import FixtureMixin


class TestRoutes(FixtureMixin):
    def test_homepage_for_anonymous(self):
        """Can watch page not authenticated user."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_pages_for_auth_user(self):
        """Can watch page authenticated user."""
        urls = (
            self.list_url,
            self.success_url,
            self.add_url,
        )
        for url in urls:
            with self.subTest(f'url: {url}'):
                response = self.auth_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_add_edit_delete_only_author(self):
        """Permission modify content only at author."""
        urls = (
            self.detail_url,
            self.edit_url,
            self.delete_url,
        )
        client_status = (
            (self.auth_client, HTTPStatus.OK),
            (self.alien_client, HTTPStatus.NOT_FOUND),
            (self.client, HTTPStatus.FOUND),
        )
        for url in urls:
            for client, status in client_status:
                with self.subTest(f'client: {client}, status: {status}'):
                    response = client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous(self):
        """Not authenticated user sent to the authentication page."""
        urls = (
            self.list_url,
            self.success_url,
            self.add_url,
            self.detail_url,
            self.edit_url,
            self.delete_url,
        )
        for url in urls:
            redirect_url = f'{self.login_url}?next={url}'
            with self.subTest(f'url: {url}'):
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_availability_pages_auth_for_all(self):
        """Pages entrance exit registration available to everyone."""
        urls = (
            self.login_url,
            self.login_url,
            self.signup_url,
        )
        clients = (self.client, self.auth_client)
        for url in urls:
            for client in clients:
                with self.subTest(f'client: {client}, url: {url}'):
                    response = client.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)
