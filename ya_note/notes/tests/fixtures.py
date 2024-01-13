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

        cls.third_user = get_user_model().objects.create(username='Tom')
        cls.user_without_note = Client()
        cls.user_without_note.force_login(cls.third_user)

        cls.alien_user = get_user_model().objects.create(username='David')
        cls.alien_client = Client()
        cls.alien_client.force_login(cls.alien_user)
        cls.data = {
            'title': 'test_1',
            'text': 'text_1',
            'slug': 'test-1',
            'author': cls.user,
        }
        cls.note = Note.objects.create(
            title='test title',
            text='test text',
            slug='test-title',
            author=cls.user
        )
        cls.list_url = reverse('notes:list')
        cls.add_url = reverse('notes:add')
        cls.home_url = reverse('notes:home')
        cls.success_url = reverse('notes:success')
        cls.detail_url = reverse('notes:detail', args=(cls.note.slug,))
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.login_url = reverse('users:login')
        cls.logout_url = reverse('users:logout')
        cls.signup_url = reverse('users:signup')

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

    def forced_creation_one_note(self):
        self.clean_note_db()
        self.note.save()

    def data_without_slug(self):
        data = self.data.copy()
        del data['slug']
        return data
