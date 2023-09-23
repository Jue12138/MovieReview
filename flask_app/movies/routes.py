from flask import Blueprint, render_template, url_for, redirect, request, flash, current_app
from flask_login import current_user
from mongoengine import *
from collections import Counter

from ..client import MovieClient
from ..forms import MovieReviewForm, SearchForm
from ..models import User, Review
from ..utils import current_time, get_b64_img

movies = Blueprint("movies", __name__)

@movies.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("movies.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@movies.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    movie_client = MovieClient(api_key=current_app.config['OMDB_API_KEY'])
    try:
        results = movie_client.search(query)
    except ValueError as e:
        return render_template("movies.index", error_msg=str(e))

    return render_template("query.html", results=results)


@movies.route("/movies/<movie_id>", methods=["GET", "POST"])
def movie_detail(movie_id):
    movie_client = MovieClient(api_key=current_app.config['OMDB_API_KEY'])
    try:
        result = movie_client.retrieve_movie_by_id(movie_id)
    except ValueError as e:
        return render_template("movie_detail.html", error_msg=str(e))

    form = MovieReviewForm()
    if form.validate_on_submit():
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=movie_id,
            movie_title=result.title,
        )

        review.save()

        return redirect(request.path)

    reviews = Review.objects(imdb_id=movie_id)
    for review in reviews:
        review.image = get_b64_img(review.commenter.username)

    return render_template(
        "movie_detail.html", form=form, movie=result, reviews=reviews
    )


@movies.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    if user is None:
        return render_template("404.html"), 404

    image = get_b64_img(username)
    reviews = Review.objects(commenter=user)
    return render_template("user_detail.html", image=image, user=user, reviews=reviews)

@movies.route("/404")
def custom_404(error):
    return render_template("404.html"), 404

##########Analytics#######

@movies.route("/analytics/most-reviewed-movies", methods=["GET"])
def most_reviewed_movies():
    movie_reviews = Review.objects.only('imdb_id', 'movie_title')
    count_by_movie = Counter((review.imdb_id, review.movie_title) for review in movie_reviews)

    most_reviewed = sorted(count_by_movie.items(), key=lambda x: x[1], reverse=True)
    data = [{"movie_id": movie[0], "movie_title": movie[1], "count": count} for (movie, count) in most_reviewed]

    return render_template("analytics_most_reviewed.html", data=data)  # Create this HTML template

@movies.route("/analytics/most-active-users", methods=["GET"])
def most_active_users():
    user_reviews = Review.objects.only('commenter')
    count_by_user = Counter(str(review.commenter.id) for review in user_reviews)

    most_active = sorted(count_by_user.items(), key=lambda x: x[1], reverse=True)
    data = [{"user_id": user_id, "count": count} for (user_id, count) in most_active]

    return render_template("analytics_most_active.html", data=data)  # Create this HTML template

@movies.route("/analytics-dashboard", methods=["GET"])
def analytics_dashboard():
    return render_template("analytics_dashboard.html")

