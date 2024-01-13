from pytils.translit import slugify

from notes.models import Note

from .fixtures import FixtureMixin


class TestLogic(FixtureMixin):
    def test_add_for_auth_user(self):
        """Correctness entered data in database."""
        self.clean_note_db()
        self.auth_client.post(self.add_url, data=self.data)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.last()
        self.assertEqual(note.title, self.data['title'])
        self.assertEqual(note.text, self.data['text'])
        self.assertEqual(note.slug, self.data['slug'])
        self.assertEqual(note.author, self.data['author'])

    def test_add_for_anonymous(self):
        """Safety data in database."""
        self.forced_creation_one_note()
        note_before = Note.objects.last()
        self.client.post(self.add_url, data=self.data)
        self.assertEqual(Note.objects.count(), 1)
        note_after = Note.objects.last()
        self.assertEqual(note_before.title, note_after.title)
        self.assertEqual(note_before.text, note_after.text)
        self.assertEqual(note_before.slug, note_after.slug)
        self.assertEqual(note_before.author, note_after.author)

    def test_auto_fill_field_slug(self):
        """Formation slug from field title."""
        self.clean_note_db()
        self.auth_client.post(self.add_url, data=self.data_without_slug())
        self.assertEqual(
            Note.objects.last().slug,
            slugify(self.data_without_slug()['title'])
        )

    def test_edit_your_notes(self):
        """Your notes available edit for author."""
        new_data = {'title': 'new title', 'text': 'new text'}
        self.auth_client.post(self.edit_url, data=new_data)
        edit_note = Note.objects.last()
        self.assertEqual(edit_note.title, new_data['title'])
        self.assertEqual(edit_note.text, new_data['text'])
        self.assertEqual(edit_note.slug, 'new-title')
        self.assertEqual(edit_note.author, self.user)

    def test_delete_your_notes(self):
        """Your notes available delete for author."""
        self.forced_creation_one_note()
        self.auth_client.post(self.delete_url)
        self.assertEqual(Note.objects.count(), 0)

    def test_modify_alien_notes(self):
        """Another users can not edit delete notes."""
        self.forced_creation_one_note()
        notes_before = Note.objects.last()
        for url in (self.edit_url, self.delete_url):
            with self.subTest(f'url: {url}'):
                self.alien_client.post(url)
                notes_after = Note.objects.last()
                self.assertEqual(Note.objects.count(), 1)
                self.assertEqual(notes_before.title, notes_after.title)
                self.assertEqual(notes_before.text, notes_after.text)
                self.assertEqual(notes_before.author, notes_after.author)

    def test_unique_slug(self):
        """Not possible create notes with same slug."""
        self.forced_creation_one_note()
        old_slug_note = Note.objects.last().slug
        self.auth_client.post(self.add_url, data={
            'title': 'some title',
            'text': 'some text',
            'author': self.user,
            'slug': old_slug_note
        }
        )
        self.assertEqual(Note.objects.count(), 1)
