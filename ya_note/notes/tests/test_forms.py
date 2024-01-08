from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm, WARNING


class TestForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = get_user_model().objects.create(username='Bob')
        cls.note = Note.objects.create(
            title='test title',
            text='test text',
            slug='test-title',
            author=cls.author,
        )
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)

    def test_exists_fields_form_note(self):
        form = NoteForm()
        texts = ('input type="text', 'textarea name="text')
        for text in texts:
            with self.subTest():
                self.assertIn(text, form.as_p())

    def test_form_validation_slug(self):
        data = {
            'title': 'valid title',
            'text': 'valid text',
            'slug': self.note.slug,
            'author': self.author
        }
        form = NoteForm(data=data)
        self.assertIn(WARNING, form.errors.get('slug')[0])

    def test_user_correct_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for name, arg in urls:
            url = reverse(name, args=arg)
            response = self.auth_client.get(url)
            with self.subTest(f'name: {name}, arg: {arg}'):
                self.assertIsInstance(response.context.get('form'), NoteForm)

    def test_uncorrect_post_for_form(self):
        self.assertEqual(Note.objects.count(), 1)
        data = {
            'title': 'valid title',
            'text': '',
            'author': self.author,
        }
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for name, arg in urls:
            url = reverse(name, args=arg)
            self.auth_client.post(url, data=data)
            with self.subTest(f'name: {name}, arg: {arg}'):
                self.assertEqual(Note.objects.count(), 1)
