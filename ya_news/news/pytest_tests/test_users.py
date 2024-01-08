from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest

pytestmark = pytest.mark.django_db


def test_create_simple_user():
    user = get_user_model().objects.create_user(
        username='Bishop',
        password='lv426',
        email='giger@alien.com',
    )
    assert user.username == 'Bishop'
    assert user.check_password('lv426')
    assert user.email == 'giger@alien.com'
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


def test_create_superuser():
    user = get_user_model().objects.create_superuser(
        username='superpuper',
        password='pupersuper',
        email='super@puper.com',
    )
    assert user.username == 'superpuper'
    assert user.check_password('pupersuper')
    assert user.email == 'super@puper.com'
    assert user.is_active
    assert user.is_staff
    assert user.is_superuser


def test_registration(client):
    data = {
        'username': 'R2D2',
        'password1': 'c-3po',
        'password2': 'c-3po'
    }
    url = reverse('users:signup')
    client.post(url, data=data)
    user = get_user_model().objects.last()
    assert len(get_user_model().objects.all()) > 0
    assert user.username == data['username']
    assert user.check_password(data['password1'])
