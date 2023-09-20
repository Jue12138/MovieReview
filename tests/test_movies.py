import pytest

from types import SimpleNamespace
import random
import string

from flask_app.forms import SearchForm, MovieReviewForm
from flask_app.models import User, Review


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200

    search = SimpleNamespace(search_query="guardians", submit="Search")
    form = SearchForm(formdata=None, obj=search)
    response = client.post("/", data=form.data, follow_redirects=True)

    assert b"Guardians of the Galaxy" in response.data


@pytest.mark.parametrize(
    ("query", "message"),
    [
        ("", "This field is required."),
        ("a" * 101, "Field must be between 1 and 100 characters long."),
    ],
)
def test_search_input_validation(client, query, message):
    search = SimpleNamespace(search_query=query, submit="Search")
    form = SearchForm(formdata=None, obj=search)
    response = client.post("/", data=form.data, follow_redirects=True)
    print(response.data)
    assert message.encode() in response.data


def test_movie_review(client, auth):
    guardians_id = "tt2015381"
    url = f"/movies/{guardians_id}"
    resp = client.get(url)
    assert resp.status_code == 200

    auth.register()
    auth.login()

    comment = "".join(random.choices(string.ascii_letters, k=20))
    review = SimpleNamespace(text=comment, submit="Enter Comment")
    form = MovieReviewForm(formdata=None, obj=review)
    response = client.post(url, data=form.data, follow_redirects=True)
    assert comment.encode() in response.data

    review_from_db = Review.objects(content=comment).first()
    assert review_from_db is not None



@pytest.mark.parametrize(
    ("movie_id", "message"),
    (
        ("12345678", "Incorrect IMDb ID."),
        ("123456789", "Incorrect IMDb ID."),
        ("1234567890", "Incorrect IMDb ID."),
    )
)
def test_movie_review_redirects(client, movie_id, message):
    url = f"/movies/{movie_id}"
    response = client.get(url)

    if movie_id == "":
        assert response.status_code == 404
        assert message.encode() in response.data
    else:
        assert response.status_code == 200
        response = client.get(url, follow_redirects=True)
        assert message.encode() in response.data


@pytest.mark.parametrize(
    ("comment", "message"),
    [
        ("", "This field is required."),
        ("a" * 4, "Field must be between 5 and 500 characters long."),
        ("a" * 501, "Field must be between 5 and 500 characters long."),
    ],
)
def test_movie_review_input_validation(client, auth, comment, message):
    guardians_id = "tt2015381"
    url = f"/movies/{guardians_id}"

    auth.register()
    auth.login()

    review = SimpleNamespace(text=comment, submit="Enter Comment")
    form = MovieReviewForm(formdata=None, obj=review)
    response = client.post(url, data=form.data, follow_redirects=True)
    assert message.encode() in response.data
