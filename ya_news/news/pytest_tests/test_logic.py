from django.urls import reverse

import pytest
from http import HTTPStatus
from pytest_django.asserts import assertRedirects

from news.forms import CommentForm, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_dispatch_comment_for_anonymous(form_data, client, news_id):
    login_url = reverse('users:login')
    url = reverse('news:detail', args=news_id)
    redirect_url = f'{login_url}?next={url}'
    response = client.post(url, data=form_data)
    assertRedirects(
        response=response,
        expected_url=redirect_url,
        status_code=HTTPStatus.FOUND,
    )


def test_dispatch_comment_for_auth(form_data, admin_client, news_id):
    url = reverse('news:detail', args=news_id)
    response = admin_client.post(url, data=form_data)
    redirect_url = f'{url}#comments'
    assertRedirects(
        response=response,
        expected_url=redirect_url,
        status_code=HTTPStatus.FOUND,
    )


def test_for_presence_forbidden_words(form_data):
    form = CommentForm(data=form_data)
    assert form.is_valid(), WARNING
    assert Comment.objects.count() == 0, (
        'Comment created with forbidden word'
    )


@pytest.mark.parametrize(
    'path, arg',
    (
        ('news:edit', pytest.lazy_fixture('news_id')),
        ('news:delete', pytest.lazy_fixture('news_id')),
    )
)
def test_availability_edit_delete_for_author(
    path,
    arg,
    form_data,
    author_client,
    comment,
):
    url = reverse(path, args=arg)
    redirect_url = f"{reverse('news:detail', args=arg)}#comments"
    response = author_client.post(url, data=form_data)
    assertRedirects(
        response=response,
        expected_url=redirect_url,
        status_code=HTTPStatus.FOUND,
    )


@pytest.mark.parametrize(
    'path, arg',
    (
        ('news:edit', pytest.lazy_fixture('news_id')),
        ('news:delete', pytest.lazy_fixture('news_id')),
    )
)
def test_availability_edit_delete_for_alien(
    path,
    arg,
    comment,
    admin_client,
    form_data
):
    url = reverse(path, args=arg)
    response = admin_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Make sure what page edit delet not allowed alien user'
    )
