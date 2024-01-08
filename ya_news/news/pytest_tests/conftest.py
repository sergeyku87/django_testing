from django.conf import settings
from django.utils import timezone

import pytest
from datetime import datetime, timedelta
from random import randint

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='test title',
        text='test text',
    )


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='some text',
    )


@pytest.fixture
def form_data(news, author):
    return {
        'news': news,
        'author': author,
        'text': 'text_for_form',
    }


@pytest.fixture
def news_id(news):
    return news.id,


@pytest.fixture
def many_news():
    news = [
        News(
            title=f'title {index}',
            text=f'text {index}',
            date=datetime.today() - timedelta(days=index),
        ) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    return News.objects.bulk_create(news)


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
    return Comment
