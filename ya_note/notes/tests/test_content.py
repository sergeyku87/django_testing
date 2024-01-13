from notes.models import Note

from .fixtures import FixtureMixin


class TestContent(FixtureMixin):
    def test_add_note_displayed_to_page_list(self):
        """Adding note on page notes when request post."""
        notes_befor = Note.objects.count()
        self.auth_client.post(self.add_url, data=self.data)
        notes_after = Note.objects.count()
        self.assertLess(notes_befor, notes_after)

    def test_for_author_notes(self):
        """Only author have access to their notes."""
        self.many_note_in_db()
        notes = Note.objects.filter(author=self.user)
        response = self.auth_client.get(self.list_url)
        obj_lst = response.context.get('object_list')
        self.assertEqual(notes.count(), obj_lst.count())
        for note_from_db, note_from_context in zip(notes, obj_lst):
            with self.subTest():
                self.assertEqual(note_from_db.title, note_from_context.title)
                self.assertEqual(note_from_db.text, note_from_context.text)
                self.assertEqual(note_from_db.slug, note_from_context.slug)
                self.assertEqual(note_from_db.author, note_from_context.author)

    def test_personal_only_notes(self):
        """Alien content not available for authors."""
        self.many_note_in_db()  # user has 6 notes, alien has 5 notes
        third = self.user_without_note.get(self.list_url)
        self.assertFalse(third.context.get('object_list'))

    def test_exist_form_for_pages_edit_delete(self):
        """Availability form for users."""
        urls = (
            self.add_url,
            self.edit_url,
        )
        for url in urls:
            with self.subTest(f'url: {url}'):
                response = self.auth_client.get(url)
                self.assertIn('form', response.context)
