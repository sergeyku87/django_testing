from django.urls import reverse

import pytest
from pytest_django.asserts import assertTemplateUsed, assertContains

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name, arg, path, view',
    (
        (
            'news:home',
            None,
            'news/home.html',
            'NewsList'),
        (
            'news:detail',
            pytest.lazy_fixture('news_id'),
            'news/detail.html',
            'NewsDetailView'
        ),
        (
            'news:edit',
            pytest.lazy_fixture('news_id'),
            'news/edit.html',
            'CommentUpdate'
        ),
        (
            'news:delete',
            pytest.lazy_fixture('news_id'),
            'news/delete.html',
            'CommentDelete'
        ),
        (
            'users:login',
            None,
            'registration/login.html',
            'LoginView'
        ),
        (
            'users:logout',
            None,
            'registration/logout.html',
            'LogoutView'
        ),
        (
            'users:signup',
            None,
            'registration/signup.html',
            'CreateView'
        ),
    )
)
def test_availability_for_template(author_client, name, arg, path, view, comment):
    url = reverse(name, args=arg)
    response = author_client.get(url)
    assert response.resolver_match.func.__name__ == view
    assertTemplateUsed(response, path)


@pytest.mark.parametrize(
    'path, arg',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('news_id')),
    )
)
def test_contains_pages(news, path, arg, admin_client):
    url = reverse(path, args=arg)
    response = admin_client.get(url)
    assertContains(
        response=response,
        text=news.text,
    )


@pytest.mark.parametrize(
    'path',
    ('users:login', 'users:signup')
)
def test_correct_form_for_page_auth(client, path):
    response = client.get(reverse(path))
    form = response.context.get('form')
    assert ('password' or 'password1') and 'username' in form.fields, (
        'Make sure what fields available for input'
    )
