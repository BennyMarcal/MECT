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
from app_sec.auth import login_required,test_password,check_password_rules
from app_sec.db import get_db

bp = Blueprint("userinfo", __name__, url_prefix="/userinfo")


@bp.route("/", methods=["GET"])
@login_required
def index():
    user = getUserInfo()
    return render_template("userinfo/info.html", user = user)

def getUserInfo():
    """Get user Info from db."""
    if g.user is not None:
        # If logged in with a local user account
        user = (
            get_db()
            .execute("SELECT id, username, email FROM user WHERE id = ?", (g.user["id"],))
            .fetchone()
        )
    elif g.github_user is not None:
        # If logged in with GitHub
        user = {
            "id": g.github_user["id"],
            "username": g.github_user["login"],
            "email": g.github_user.get("email"),
            "github_username": g.github_user["login"],
        }
    else:
        # Redirect to login if not logged in
        return redirect(url_for("auth.login"))

    return user

@bp.route("/update", methods=("GET", "POST"))
@login_required
def update():
    user = getUserInfo()
    """Update user info.
    """
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        old_password = request.form["old_password"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        error = None

        if not username:
            error = "Username is required."

        if not email or not "@" in email:
            error = "Invalid email format."
        
        if password != confirm_password:
            error = "Passwords don't match."

        if not test_password(old_password):
            error = "Old password is incorrect."

        if password and not check_password_rules(password):
            error = "Password does not meet the requirements."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            if password:
                db.execute(
                    "UPDATE user SET username = ?, email = ?, password = ? WHERE id = ?", (username, email, generate_password_hash(password), g.user["id"])
                )
            else:
                db.execute(
                    "UPDATE user SET username = ?, email = ? WHERE id = ?", (username, email, g.user["id"])
                )
            db.commit()
            return redirect(url_for("userinfo.index"))

    return render_template("userinfo/update.html", user = user)


@bp.route("/orders", methods=["GET"])
@login_required
def orders():
    if g.user is None:
        return redirect(url_for("auth.login"))

    db = get_db()

    orders = get_db().execute(
        "SELECT * FROM orders WHERE cart_id IN (SELECT id FROM cart WHERE user_id = ?)", (g.user["id"],)
    ).fetchall()

    return render_template("userinfo/orders.html", orders = orders)


@bp.route("/delete", methods=["POST"])
@login_required
def delete():
    if(test_password(request.form["password"])):
        """Delete a user."""
        db = get_db()
        db.execute("DELETE FROM orders WHERE cart_id IN (SELECT id FROM cart WHERE user_id = ?)", (g.user["id"],))
        db.execute("DELETE FROM cart_item WHERE cart_id IN (SELECT id FROM cart WHERE user_id = ?)", (g.user["id"],))
        db.execute("DELETE FROM cart WHERE user_id = ?", (g.user["id"],))
        db.execute("DELETE FROM reviews WHERE author_id = ?", (g.user["id"],))
        db.execute("DELETE FROM user WHERE id = ?", (g.user["id"],))
        db.commit()
        return redirect(url_for("userinfo.index"))
    else:
        flash("Password is incorrect.")
        return redirect(url_for("userinfo.update"))
