from django.contrib.auth import get_user_model

import pytest


@pytest.mark.django_db
def test_registration(client, signup_url):
    """Correct fill form authenticated."""
    data = {
        'username': 'R2D2',
        'password1': 'c-3po',
        'password2': 'c-3po'
    }
    assert get_user_model().objects.count() == 0
    client.post(signup_url, data=data)
    assert get_user_model().objects.count() > 0
    user = get_user_model().objects.last()
    assert user.username == data['username']
    assert user.check_password(data['password1'])
