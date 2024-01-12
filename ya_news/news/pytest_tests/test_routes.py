import pytest
from pytest_django.asserts import assertRedirects

from http import HTTPStatus

from test_logic import FORM_DATA

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url',
    (
        (pytest.lazy_fixture('home_url')),
        (pytest.lazy_fixture('detail_url')),
        (pytest.lazy_fixture('login_url')),
        (pytest.lazy_fixture('logout_url')),
        (pytest.lazy_fixture('signup_url')),
    )
)
def test_availability_pages_for_anonymous(url, client, news):
    """Not authenticated user can view some pages."""
    assert client.get(url).status_code == HTTPStatus.OK, (
        f'Make sure it is availability {url} for anonymous'
    )


@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('edit_url'),
        pytest.lazy_fixture('delete_url'),
    )
)
def test_private_pages_for_anonymoys(
    url,
    client,
    login_url,
    comment
):
    """Not authenticated user must authenticate for view this pages."""
    assertRedirects(
        response=client.get(url),
        expected_url=f'{login_url}?next={url}',
        status_code=HTTPStatus.FOUND,
    )


@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('edit_url'),
        pytest.lazy_fixture('delete_url'),
    )
)
@pytest.mark.parametrize(
    'caller, status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
    )
)
def test_pages_with_different_level_available_for_users(
    url,
    caller,
    status,
    comment
):
    """Author and not author have different rights."""
    assert caller.get(url).status_code == status, (
        f'Make sure it is availability {url} for {caller}'
    )


def test_dispatch_comment_for_anonymous(
    client,
    news,
    login_url,
    detail_url,
):
    """Not authenticated user must authenticate."""
    assertRedirects(
        response=client.post(detail_url, data=FORM_DATA),
        expected_url=f'{login_url}?next={detail_url}',
        status_code=HTTPStatus.FOUND,
    )


def test_dispatch_comment_for_auth(
    admin_client,
    news,
    detail_url,
):
    """Authenticated user can leave comment."""
    assertRedirects(
        response=admin_client.post(detail_url, data=FORM_DATA),
        expected_url=f'{detail_url}#comments',
        status_code=HTTPStatus.FOUND,
    )


@pytest.mark.parametrize(
    'url',
    (
        (pytest.lazy_fixture('edit_url')),
        (pytest.lazy_fixture('delete_url')),
    )
)
def test_request_on_modify_for_author(
    url,
    author_client,
    comment,
    detail_url,
):
    """Author comment can edit delete own comments."""
    redirect_url = f"{detail_url}#comments"
    response = author_client.post(url, data=FORM_DATA)
    assertRedirects(
        response=response,
        expected_url=redirect_url,
        status_code=HTTPStatus.FOUND,
    )


@pytest.mark.parametrize(
    'url',
    (
        (pytest.lazy_fixture('edit_url')),
        (pytest.lazy_fixture('delete_url')),
    )
)
def test_request_modify_for_alien(
    url,
    comment,
    admin_client,
):
    """Not author not can edit delete comments."""
    response = admin_client.post(url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Make sure what page edit delet not allowed alien user'
    )
