from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


class FixtureMixin(TestCase):
    COUNT_NOTES = 5

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(username='Bob')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)

        cls.alien_user = get_user_model().objects.create(username='David')
        cls.alien_client = Client()
        cls.alien_client.force_login(cls.alien_user)
        cls.data = {
            'title': 'test_1',
            'text': 'text_1',
            'slug': 'test-1',
            'author': cls.user,
        }

    def setUp(self):
        self.note = Note.objects.create(
            title='test title',
            text='test text',
            slug='test-title',
            author=self.user
        )
        self.list_url = reverse('notes:list')
        self.add_url = reverse('notes:add')
        self.home_url = reverse('notes:home')
        self.success_url = reverse('notes:success')
        self.detail_url = reverse('notes:detail', args=(self.note.slug,))
        self.edit_url = reverse('notes:edit', args=(self.note.slug,))
        self.delete_url = reverse('notes:delete', args=(self.note.slug,))
        self.login_url = reverse('users:login')
        self.logout_url = reverse('users:logout')
        self.signup_url = reverse('users:signup')

    def tearDown(self):
        Note.objects.all().delete()

    def many_note_in_db(self):
        [
            Note.objects.create(
                title=f'title {index}',
                text=f'text {index}',
                slug=f'title-{user}-{index}',
                author=user,
            )
            for user in (self.user, self.alien_user)
            for index in range(self.COUNT_NOTES)
        ]

    def clean_note_db(self):
        Note.objects.all().delete()
