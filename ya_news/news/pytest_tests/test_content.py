from django.conf import settings
from django.urls import reverse

import pytest

pytestmark = pytest.mark.django_db


def test_coutn_news_on_page(many_news, client):
    response = client.get(reverse('news:home'))
    count_news = len(response.context.get('object_list'))
    assert settings.NEWS_COUNT_ON_HOME_PAGE == count_news, (
        'Number news exceeds allowed value'
    )


def test_date_ordering(many_news, client):
    response = client.get(reverse('news:home'))
    dates_in_context = [
        news.date for news in response.context.get('object_list')
    ]
    expected_dates = sorted(dates_in_context, reverse=True)
    assert dates_in_context == expected_dates, (
        'Make sure that news sorted in descending order'
    )


def test_chronological_ordering_comments(many_comments):
    comment_first = many_comments.objects.first()
    comment_last = many_comments.objects.last()
    assert comment_first.created < comment_last.created, (
        'Make sure that comments in correct chronological order'
    )


def test_form_comment_for_anonymous(client, news_id):
    url = reverse('news:detail', args=news_id)
    response = client.get(url)
    assert 'form' not in response.context, (
        'Form should not be available for anonymous user'
    )


def test_form_comment_for_auth_user(admin_client, news_id):
    url = reverse('news:detail', args=news_id)
    response = admin_client.get(url)
    assert 'form' in response.context, (
        'Form should not be available for anonymous user'
    )
