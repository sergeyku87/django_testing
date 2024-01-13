from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils import timezone


import pytest
from datetime import datetime, timedelta
from random import randint

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def author_client(author):
    author_client = Client()
    author_client.force_login(author)
    return author_client


@pytest.fixture
def news():
    yield News.objects.create(
        title='test title',
        text='test text',
    )
    News.objects.all().delete()


@pytest.fixture
def comment(news, author):
    yield Comment.objects.create(
        news=news,
        author=author,
        text='some text',
    )
    Comment.objects.all().delete()


@pytest.fixture
def many_news():
    yield News.objects.bulk_create(
        News(
            title=f'title {index}',
            text=f'text {index}',
            date=datetime.today() - timedelta(days=index),
        ) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    News.objects.all().delete()


@pytest.fixture
def many_comments(news, admin_user):
    for index in range(randint(3, 7)):
        comment = Comment.objects.create(
            news=news,
            author=admin_user,
            text=f'text {index}',
        )
        comment.created = timezone.now() - timedelta(days=index)
        comment.save()
    yield Comment.objects.all()
    Comment.objects.all().delete()


@pytest.fixture
def delete_url(news):
    return reverse('news:delete', args=(news.id,))


@pytest.fixture
def edit_url(news):
    return reverse('news:edit', args=(news.id,))


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')
