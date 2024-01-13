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
    news,
):
    """Correct fields for add comment."""
    news.comment_set.all().delete()
    admin_client.post(detail_url, data=FORM_DATA)
    assert news.comment_set.count() == 1
    comment = news.comment_set.last()
    assert comment.text == FORM_DATA['text']
    assert comment.author == admin_user
    assert comment.news == news


def test_add_comment_for_anonymous_user(client, detail_url, news):
    """Not authenticated user not can add comment."""
    news.comment_set.all().delete()
    client.post(detail_url, data=FORM_DATA)
    assert news.comment_set.count() == 0


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
    assert news.comment_set.count() == 1
    comment_befor = news.comment_set.last()
    client.post(delete_url)
    assert news.comment_set.count() == 1
    comment_after = news.comment_set.last()
    assert comment_after.news == comment_befor.news
    assert comment_after.author == comment_befor.author
    assert comment_after.text == comment_befor.text


def test_on_edit_for_author(
    author_client,
    author,
    news,
    comment,
    edit_url,
):
    """Author commetn can edit comment."""
    assert news.comment_set.count() == 1
    author_client.post(edit_url, data=FORM_DATA)
    assert news.comment_set.count() == 1
    comment = news.comment_set.last()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_on_edit_for_notauthor(
    admin_client,
    news,
    comment,
    edit_url,
):
    """Not author commetn not can edit comment."""
    assert news.comment_set.count() == 1
    comment_befor = news.comment_set.last()
    admin_client.post(edit_url, data=FORM_DATA)
    assert news.comment_set.count() == 1
    comment_after = news.comment_set.last()
    assert comment_befor.text == comment_after.text
    assert comment_befor.news == comment_after.news
    assert comment_befor.author == comment_after.author


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
