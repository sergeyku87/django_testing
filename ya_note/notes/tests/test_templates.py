from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note


class TestHtml(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = get_user_model().objects.create(username='Bob')
        cls.note = Note.objects.create(
            title='test title',
            text='test text',
            author=cls.author,
        )
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.name_paths = (
            ('notes:home', None, 'notes/home.html'),
            ('notes:add', None, 'notes/form.html'),
            ('notes:edit', (cls.note.slug,), 'notes/form.html'),
            ('notes:detail', (cls.note.slug,), 'notes/detail.html'),
            ('notes:delete', (cls.note.slug,), 'notes/delete.html'),
            ('notes:list', None, 'notes/list.html'),
            ('notes:success', None, 'notes/success.html'),
            ('users:login',  None, 'registration/login.html'),
            ('users:logout', None, 'registration/logout.html'),
            ('users:signup', None, 'registration/signup.html'),
        )
        cls.contains = (
            ('notes:home', None, 'Проект YaNote поможет вам не забыть о самом важном!'),
            ('notes:add', None, 'Добавить'),
            ('notes:edit', (cls.note.slug,), 'Редактировать'),
            ('notes:detail', (cls.note.slug,), f'Заметка ID: {cls.note.id}'),
            ('notes:delete', (cls.note.slug,), f'Удалить заметку {cls.note.id}?'),
            ('notes:list', None, 'Список заметок'),
            ('notes:success', None, 'Успешно'),
            ('users:login', None, 'Войти на сайт'),
            ('users:logout', None, 'Вы вышли из своей учётной записи. Ждём вас снова!'),
            ('users:signup', None, 'Зарегистрироваться'),
        )

    def test_availability_templates(self):
        for name, arg, template in self.name_paths:
            url = reverse(name, args=arg)
            response = self.auth_client.get(url)
            with self.subTest(f'name: {name}'):
                self.assertTemplateUsed(response, template)

    def test_contains_pages(self):
        for name, arg, content in self.contains:
            url = reverse(name, args=arg)
            response = self.auth_client.get(url)
            with self.subTest(f'name: {name}, content: {content}'):
                self.assertContains(
                    response=response,
                    text=content,
                    )
