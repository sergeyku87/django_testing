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
        for note_1, note_2 in zip(notes, obj_lst):
            with self.subTest():
                self.assertEqual(note_1.title, note_2.title)
                self.assertEqual(note_1.text, note_2.text)
                self.assertEqual(note_1.slug, note_2.slug)
                self.assertEqual(note_1.author, note_2.author)

    def test_personal_only_notes(self):
        """Alien content not available for authors."""
        self.many_note_in_db()
        user = self.auth_client.get(self.list_url)
        alien = self.alien_client.get(self.list_url)
        inner_join = user.context.get(
            'object_list'
        ).intersection(
            alien.context.get('object_list')
        )
        self.assertFalse(inner_join)

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
