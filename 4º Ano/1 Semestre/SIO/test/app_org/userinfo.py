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
from app_org.auth import login_required
from app_org.db import get_db

bp = Blueprint("userinfo", __name__, url_prefix="/userinfo")


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    user = getUserInfo()
    return render_template("userinfo/info.html", user = user)

def getUserInfo():
    """Get user Info from db.
    """
    if g.user is None:
        return redirect(url_for("auth.login"))
    user = (
      get_db()
      .execute(
        "SELECT id,username,email FROM user WHERE id = ?", (g.user["id"],)
        ).fetchone()
      )
    
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
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        error = None

        if not username:
            error = "Username is required."

        if not email or not "@" in email:
            error = "Invalid email format."
        
        if password != confirm_password:
            error = "Passwords don't match."

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


@bp.route("/orders", methods=("GET", "POST"))
@login_required
def orders():
    if g.user is None:
        return redirect(url_for("auth.login"))

    db = get_db()

    orders = get_db().execute(
        "SELECT * FROM orders WHERE cart_id IN (SELECT id FROM cart WHERE user_id = ?)", (g.user["id"],)
    ).fetchall()

    return render_template("userinfo/orders.html", orders = orders)


@bp.route("/<int:id>/delete", methods=("GET", "POST"))
@login_required
def delete(id):
    """Delete a user."""
    #getUserInfo(id)
    db = get_db()
    db.execute("DELETE FROM user WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("userinfo.index"))
