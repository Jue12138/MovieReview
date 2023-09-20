from flask import Blueprint, session, request, redirect, url_for
from flask_oauthlib.client import OAuth
from flask_login import login_user
import secrets

google = Blueprint("google", __name__)
oauth = OAuth()

# Google OAuth setup should go in the create_app or a similar function where 'app' is available.
def setup_google_oauth(app):
    if not app.config.get('TESTING'):
        global google_oauth
        google_oauth = oauth.remote_app(
            'google',
            consumer_key=app.config.get('GOOGLE_CLIENT_ID'),
            consumer_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
            request_token_params={
                'scope': 'email',
            },
            base_url='https://www.googleapis.com/oauth2/v1/',
            request_token_url=None,
            access_token_method='POST',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            authorize_url='https://accounts.google.com/o/oauth2/auth',
        )

        @google_oauth.tokengetter
        def get_google_oauth_token():
            return session.get('access_token')

@google.route('/set_session')
def set_session_value():
    session['key'] = 'value'
    return 'Session value set!'

@google.route('/login/google')
def login_google():
    return google_oauth.authorize(callback=url_for('google.google_authorized', _external=True))

@google.route('/login/google/authorized')
def google_authorized():
    response = google_oauth.authorized_response()
    if response is None or response.get('access_token') is None:
        error_reason = request.args.get('error_reason', 'Unknown reason')
        error_description = request.args.get('error_description', 'Unknown error')
        return f'Access denied: reason={error_reason} error={error_description}'

    session['access_token'] = response['access_token']

    me = google_oauth.get('userinfo')
    user_info = me.data

    from ..models import User

    user = User.objects(email=user_info['email']).first()
    if user:
        login_user(user)
    else:
        password = secrets.token_hex(12 // 2)
        user = User(email=user_info['email'], username=user_info['email'], password=password)
        user.save()
        login_user(user)

    return redirect(url_for('users.account'))

