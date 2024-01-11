from django.conf import settings

import pytest

pytestmark = pytest.mark.django_db


def test_coutn_news_on_page(
    many_news,
    client,
    home_url,
):
    """Displayed news no more specified count."""
    count_news = client.get(home_url).context.get('object_list').count()
    assert settings.NEWS_COUNT_ON_HOME_PAGE == count_news, (
        'Number news exceeds allowed value'
    )


def test_date_ordering(
    many_news,
    client,
    home_url,
):
    """Order news from fresh to old."""
    dates = [
        news.date for news in client.get(home_url).context.get('object_list')
    ]
    assert dates == sorted(dates, reverse=True), (
        'Make sure that news sorted in descending order'
    )


def test_chronological_ordering_comments(
    many_comments,
    detail_url,
    client,
):
    """Order comments from old to fresh."""
    dates = [
        i.created for i in client.get(
            detail_url
        ).context.get('object').comment_set.all()
    ]
    assert dates == sorted(dates), (
        'Make sure that comments in correct chronological order'
    )


def test_form_comment_for_anonymous(client, detail_url):
    """Available form comment for not authenticated user."""
    assert 'form' not in client.get(detail_url).context, (
        'Form should not be available for anonymous user'
    )


def test_form_comment_for_auth_user(
    admin_client,
    news,
    detail_url,
):
    """Available form comment for authenticated user."""
    assert 'form' in admin_client.get(detail_url).context, (
        'Form should not be available for anonymous user'
    )
