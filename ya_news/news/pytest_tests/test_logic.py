import pytest
from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING

pytestmark = pytest.mark.django_db


FORM_DATA = {
    'text': 'text_for_form',
}


def test_add_comment_for_auth_user(
    admin_client,
    admin_user,
    detail_url,
    news
):
    """Correct fields for add comment."""
    count_befor = news.comment_set.count()
    admin_client.post(detail_url, data=FORM_DATA)
    assert news.comment_set.count() == count_befor + 1
    assert news.comment_set.last().text == FORM_DATA['text']
    assert news.comment_set.last().author == admin_user
    assert news.comment_set.last().news == news


def test_add_comment_for_anonymous_user(client, detail_url, news):
    """Not authenticated user not can add comment."""
    count_befor = news.comment_set.count()
    client.post(detail_url, data=FORM_DATA)
    assert news.comment_set.count() == count_befor


def test_on_delete_for_author(
    news,
    comment,
    author_client,
    delete_url,
):
    """Authenticated user can delete comment."""
    assert news.comment_set.count() == 1
    author_client.post(delete_url)
    assert news.comment_set.count() == 0


def test_on_delete_for_anonymous(
    news,
    comment,
    client,
    delete_url,
):
    """Not authenticated user not can delete comment."""
    comment_befor = news.comment_set.last()
    assert news.comment_set.count() == 1
    client.post(delete_url)
    assert news.comment_set.count() == 1
    assert news.comment_set.last().news == comment_befor.news
    assert news.comment_set.last().author == comment_befor.author
    assert news.comment_set.last().text == comment_befor.text


def test_on_edit_for_author(
    author_client,
    author,
    news,
    comment,
    edit_url,
):
    """Author commetn can edit comment."""
    author_client.post(edit_url, data=FORM_DATA)
    assert news.comment_set.last().text == FORM_DATA['text']
    assert news.comment_set.last().news == news
    assert news.comment_set.last().author == author


def test_on_edit_for_notauthor(
    admin_client,
    news,
    comment,
    edit_url,
):
    """Not author commetn not can edit comment."""
    comment_befor = news.comment_set.last()
    admin_client.post(edit_url, data=FORM_DATA)
    assert comment_befor.text == news.comment_set.last().text
    assert comment_befor.news == news.comment_set.last().news
    assert comment_befor.author == news.comment_set.last().author


def test_for_presence_forbidden_words(admin_client, detail_url):
    """Comment with forbidden words not can created."""
    data = FORM_DATA.copy()
    data['text'] = BAD_WORDS[0]
    assertFormError(
        response=admin_client.post(detail_url, data=data),
        form='form',
        field='text',
        errors=WARNING,
    )
