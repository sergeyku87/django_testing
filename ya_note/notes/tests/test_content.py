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
        for i, j in zip(notes, obj_lst):
            with self.subTest():
                self.assertEqual(i.title, j.title)
                self.assertEqual(i.text, j.text)
                self.assertEqual(i.slug, j.slug)
                self.assertEqual(i.author, j.author)

    def test_personal_only_notes(self):
        """Alien content not available for authors."""
        self.many_note_in_db()
        user = self.auth_client.get(self.list_url)
        alien = self.alien_client.get(self.list_url)
        first = set([
            obj.author.username for obj in user.context.get('object_list')
        ])
        second = set([
            obj.author.username for obj in alien.context.get('object_list')
        ])
        self.assertEqual(len(first), len(second))
        self.assertNotEqual(first, second)

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
