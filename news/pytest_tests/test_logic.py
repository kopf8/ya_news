from django.urls import reverse
from http import HTTPStatus

import pytest
import random
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
        client, detail_news_url, form_data
):
    response = client.post(detail_news_url, data=form_data)
    login_url = reverse('users:login')
    assertRedirects(
        response,
        f'{login_url}?next={detail_news_url}',
        status_code=302,
        target_status_code=200,
        msg_prefix='',
        fetch_redirect_response=True
    )
    assert Comment.objects.count() == 0


def test_user_can_create_comment(author_client, author, detail_news_url, news,
                                 form_data):
    response = author_client.post(detail_news_url, data=form_data)
    assertRedirects(response, f'{detail_news_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.last()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, detail_news_url):
    bad_words_data = {'text': f'Какой-то текст, {random.choice(BAD_WORDS)}, '
                              f'еще текст'}
    response = author_client.post(detail_news_url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(
        author_client, delete_comment_url, detail_news_url
):
    response = author_client.delete(delete_comment_url)
    assertRedirects(response, f'{detail_news_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(
        reader_client, delete_comment_url
):
    response = reader_client.delete(delete_comment_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def anonymous_user_cant_delete_comment(
        client, delete_comment_url):
    response = client.delete(delete_comment_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
    author_client, form_data, comment, edit_comment_url, detail_news_url
):
    response = author_client.post(edit_comment_url, data=form_data)
    assertRedirects(response, f'{detail_news_url}#comments')
    comment.refresh_from_db()
    assert comment.text == 'Новый текст'


def test_user_cant_edit_comment_of_another_user(
    reader_client, form_data, comment, edit_comment_url
):
    response = reader_client.post(edit_comment_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == 'Текст'


def anonymous_user_cant_edit_comment(
    client, form_data, comment, edit_comment_url
):
    response = client.post(edit_comment_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == 'Текст'
