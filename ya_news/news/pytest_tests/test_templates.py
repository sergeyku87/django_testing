import pytest
from pytest_django.asserts import assertTemplateUsed, assertContains

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, path, view',
    (
        (
            pytest.lazy_fixture('home_url'),
            'news/home.html',
            'NewsList'),
        (
            pytest.lazy_fixture('detail_url'),
            'news/detail.html',
            'NewsDetailView'
        ),
        (
            pytest.lazy_fixture('edit_url'),
            'news/edit.html',
            'CommentUpdate'
        ),
        (
            pytest.lazy_fixture('delete_url'),
            'news/delete.html',
            'CommentDelete'
        ),
        (
            pytest.lazy_fixture('login_url'),
            'registration/login.html',
            'LoginView'
        ),
        (
            pytest.lazy_fixture('logout_url'),
            'registration/logout.html',
            'LogoutView'
        ),
        (
            pytest.lazy_fixture('signup_url'),
            'registration/signup.html',
            'CreateView'
        ),
    )
)
def test_availability_for_template(
    author_client,
    path,
    url,
    view,
    comment,
):
    """Accordance name url, path url, view function."""
    response = author_client.get(url)
    assert response.resolver_match.func.__name__ == view
    assertTemplateUsed(response, path)


@pytest.mark.parametrize(
    'url',
    (
        (pytest.lazy_fixture('home_url')),
        (pytest.lazy_fixture('detail_url')),
    )
)
def test_contains_pages(news, url, admin_client):
    """On pages displayed correct contains."""
    response = admin_client.get(url)
    assertContains(
        response=response,
        text=news.text,
    )


@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('login_url'),
        pytest.lazy_fixture('signup_url'),
    )
)
def test_correct_form_for_page_auth(client, url):
    """Pages login, signup contain form to fill in."""
    response = client.get(url)
    form = response.context.get('form')
    assert ('password' or 'password1') and 'username' in form.fields, (
        'Make sure what fields available for input'
    )
