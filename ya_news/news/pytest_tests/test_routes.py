from django.urls import reverse

import pytest
from pytest_django.asserts import assertRedirects

from http import HTTPStatus

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'path, arg',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('news_id')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    )
)
def test_availability_pages_for_anonymous(path, arg, client):
    url = reverse(path, args=arg)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'Make sure it is availability {url} for anonymous'
    )


@pytest.mark.parametrize(
    'path, arg',
    (
        ('news:edit', pytest.lazy_fixture('news_id')),
        ('news:delete', pytest.lazy_fixture('news_id')),
    )
)
def test_pages_edit_delete_comment_for_anonymoys(path, arg, client, comment):
    url = reverse(path, args=arg)
    login_url = reverse('users:login')
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
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
@pytest.mark.parametrize(
    'caller, code',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
    )
)
def test_pages_edit_del_comment_for_author_and_notauthor(
    path,
    arg,
    caller,
    code,
    comment
):
    url = reverse(path, args=arg)
    response = caller.get(url)
    assert response.status_code == code, (
        f'Make sure it is availability {url} for {caller}'
    )
