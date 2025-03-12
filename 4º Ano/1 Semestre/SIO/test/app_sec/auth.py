import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_oauthlib.client import OAuth

from app_sec.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

# Initialize Flask-OAuthlib
oauth = OAuth()

# GitHub as OAuth provider
github = oauth.remote_app(
    'github',
    consumer_key='86b229eeaac688167178',
    consumer_secret='5058f1c291f7ba1de21ce91af7d11ff5e3857226',
    request_token_params=None,
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)

@bp.route('/login_with_github')
def login_with_github():
    return github.authorize(callback=url_for('auth.github_callback', _external=True))

@bp.route('/github/callback')
def github_callback():
    response = github.authorized_response()
    if response is None or response.get('access_token') is None:
        flash('Authorization failed: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(url_for('index'))

    # Save the user's GitHub information in the session
    session['github_token'] = (response['access_token'], '')
    user_info = github.get('user')
    github_username = user_info.data['login']  # GitHub username
    session['user_id'] = github_username  # Use GitHub username as user_id
    return redirect(url_for('index'))

@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view



@bp.before_app_request
def load_logged_in_user():
    """Load the logged-in user from the session or GitHub."""
    user_id = session.get("user_id")

    if user_id:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )
    else:
        g.user = None

    if "github_token" in session:
        github_user = github.get("user")
        g.github_user = github_user.data if github_user else None
    else:
        g.github_user = None

def check_password_rules(password):
    """Checks if password meets rules"""
    if len(password) < 12:
        return False
    elif len(password) > 128:
        return False
    else:
        return True

@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        if not check_password_rules(password):
            error = "Password does not meet requirements."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User {username} is already registered."
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")

def test_password(password):
    """Tests if is user password"""
    
    db = get_db()
    error = None
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (g.user["username"],)
    ).fetchone()

    if user is None:
        error = "Incorrect username."
    elif not check_password_hash(user["password"], password):
        error = "Incorrect password."

    if error is None:
        return True
    else:
        return False

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
