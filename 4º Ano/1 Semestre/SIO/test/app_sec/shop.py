import functools
import re
import os

from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    Blueprint,
    g,
    render_template,
    session,
)
from app_sec.db import get_db
from app_sec.auth import login_required
from werkzeug.utils import secure_filename
from app_sec.auth import test_password

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static'

bp = Blueprint("shop", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    #products = all
    products = get_all_products()
    
    if request.method == "POST":
        search_result = request.form.get("search_result", "").strip()
     
        if search_result:
            if validate_search_query(search_result): #if valid query
                products = search_products(search_result) 
            else:
                flash("Invalid search query") 
            if not products: #if no products found
                flash("Product not found")
                products = get_all_products() #show all products

    return render_template("shop/productslist.html", products=products)

def validate_search_query(query):
    pattern = r"^[A-Za-z0-9\s-]+$"
    return re.match(pattern, query)

def search_products(query):
    db = get_db()
    query = f"%{query}%"
    return db.execute(
        "SELECT * FROM products WHERE productname LIKE ? OR category LIKE ?",
        (query, query),
    ).fetchall()


def get_all_products():
    db = get_db()
    return db.execute("SELECT * FROM products").fetchall()

@bp.route("/add", methods=("GET", "POST"))
# @login_required
def add():
    if g.user is None:
        # quando um user não logado tenta aceder á pagina de adicionar produtos,
        # deve ser redirecionado para uma pagina de erro
        return render_template("error.html")

    if g.user["role"] == "admin":
        if request.method == "POST":
            productname = request.form["productname"]
            info = request.form["info"]
            price = request.form["price"]
            quantity = request.form["quantity"]
            category = request.form["category"]
            img = request.files["img"]

            error = None

            if not productname:
                error = "Name is required."
            if not price:
                error = "Price is required."
            if not quantity:
                error = "Quantity is required."
            if img and allowed_file(img.filename):
                save_image(img)
                image = secure_filename(img.filename)
            else:
                image = None

            if error is not None:
                flash(error)
            else:
                db = get_db()
                db.execute(
                    "INSERT INTO products (productname, price, info, quantity, category, img) VALUES (?, ?, ?, ?, ?, ?)",
                    (productname, price, info, quantity, category, image),
                )
                db.commit()
                return redirect(url_for("shop.index"))

        return render_template("shop/add.html")
    else:
        return render_template("error.html")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "jpg",
        "jpeg",
        "png",
        "gif",
    }


def save_image(img):
    img.save(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            app.config["UPLOAD_FOLDER"],
            secure_filename(img.filename),
        )
    )


@bp.route("/<string:name>/", methods=("GET", "POST"))
def productinfo(name):
    """Shows product info."""
    product = (
        get_db()
        .execute("SELECT * FROM products WHERE productname = ?", (name,))
        .fetchone()
    )

    if product is not None:

        """gets reviews for product"""
        reviews = (
            get_db()
            .execute("SELECT * FROM reviews WHERE product_id = ?", (product["id"],))
            .fetchall()
        )

        """calculate the average rating of each product"""
        avg_rating = 0
        total = 0
        n_ratings = 0
        reviews = (
            get_db()
            .execute("SELECT * FROM reviews WHERE product_id = ?", (product["id"],))
            .fetchall()
        )

        if len(reviews) > 0:
            for review in reviews:
                total += review["rating"]
                n_ratings += 1

        if n_ratings > 0:
            avg_rating = total / n_ratings

        avg_rating = int(avg_rating)

        return render_template(
            "shop/productinfo.html", product=product, reviews=reviews, avg_rating=avg_rating
        )

    else:
        return render_template("error.html")

@bp.route("/removefromcart/<int:product_id>/", methods=("GET", "POST"))
def removefromcart(product_id):
    db = get_db()

    # Get the active cart for the user
    cart_id = db.execute(
        "SELECT id FROM cart WHERE user_id = ? AND cart_status = 'active'",
        (g.user["id"],),
    ).fetchone()

    if cart_id is not None:
        # Check if the product is already in the cart
        cart_item = db.execute(
            "SELECT id, quantity FROM cart_item WHERE cart_id = ? AND product_id = ?",
            (cart_id[0], product_id),
        ).fetchone()

        if cart_item is not None:
            # Decrease the quantity of the specified product in the cart by 1
            updated_quantity = cart_item["quantity"] - 1
            if updated_quantity > 0:
                db.execute(
                    "UPDATE cart_item SET quantity = ? WHERE id = ?",
                    (updated_quantity, cart_item["id"]),
                )
            else:
                # If the quantity becomes zero, remove the item from the cart
                db.execute(
                    "DELETE FROM cart_item WHERE id = ?",
                    (cart_item["id"],),
                )

            db.commit()

            # Update the cart total
            update_cart_total(db, cart_id[0])

        return redirect(url_for("shop.cart"))

    return render_template("error.html")


@bp.route("/addtocart", methods=("GET", "POST"))
def addtocart():
    db = get_db()
    # checks if user has a cart open
    cart_id = db.execute(
        "SELECT id FROM cart WHERE user_id = ? AND cart_status = 'active'",
        (g.user["id"],),
    ).fetchone()

    # if the user doens't have a cart open, create one
    if cart_id is None:
        db.execute("INSERT INTO cart (user_id) VALUES (?)", (g.user["id"],))

        db.commit()

        cart_id = db.execute("select last_insert_rowid()").fetchone()

    """Adds product to cart_items"""
    if request.method == "POST":
        product_id = request.form["product_id"]
        cart_quantity = request.form["quantity"]
        product_name = request.form["product_name"]

        error = None

        if not cart_quantity:
            error = "Quantity is required."
        if error is not None:
            flash(error)
        else:
            # Check if the product is already in the user's cart
            cart_item = db.execute(
                "SELECT id, quantity FROM cart_item WHERE cart_id = ? AND product_id = ?",
                (cart_id[0], product_id),
            ).fetchone()

            product = db.execute(
                "SELECT quantity FROM products WHERE id = ?",
                (product_id,),
            ).fetchone()

            if product['quantity'] == 0:
                flash("This product is out of stock.")

            if cart_item is not None:
                # If the product is in the cart, increment the quantity
                updated_quantity = cart_item['quantity'] + int(cart_quantity)

                if updated_quantity > product['quantity']:
                    flash("You can't add more of this product to your cart.")
                else:
                    db.execute(
                        "UPDATE cart_item SET quantity = ? WHERE id = ?",
                        (updated_quantity, cart_item['id']),
                    )
            else:
                # If the product is not in the cart, insert a new record
                db.execute(
                    "INSERT INTO cart_item (cart_id, product_id, quantity) VALUES (?, ?, ?)",
                    (cart_id[0], product_id, cart_quantity),
                )
            db.commit()
            
            # update cart total
            update_cart_total(db, cart_id[0])

            return redirect(url_for("shop.productinfo", name=product_name))

    # SHOULD RETURN TO ERROR PAGE
    return render_template("error.html")


def update_cart_total(db, cart_id):
    """Update the total of the cart in the database."""
    total_price = db.execute(
        "SELECT SUM(products.price * cart_item.quantity) FROM cart_item "
        "JOIN products ON cart_item.product_id = products.id "
        "WHERE cart_item.cart_id = ?",
        (cart_id,),
    ).fetchone()[0]

    db.execute(
        "UPDATE cart SET total = ? WHERE id = ?",
        (total_price or 0, cart_id),
    )
    db.commit()


@bp.route("/cart", methods=("GET", "POST"))
@login_required
def cart(): 
    """Shows cart info."""
    # checks if user has a cart open
    cart_id = (
        get_db()
        .execute(
            "SELECT id FROM cart WHERE user_id = ? AND cart_status = 'active'",
            (g.user["id"],),
        )
        .fetchone()
    )

    # if the user doens't have a cart open, create one
    if cart_id is None:
        get_db().execute("INSERT INTO cart (user_id) VALUES (?)", (g.user["id"],))

        get_db().commit()

        cart_id = get_db().execute("select last_insert_rowid()").fetchone()

    cart_items = (
        get_db()
        .execute(
            "SELECT * FROM cart_item JOIN products ON cart_item.product_id = products.id WHERE cart_item.cart_id = ?",
            (cart_id[0],),
        )
        .fetchall()
    )

    # calculate total price
    total_price = 0
    for item in cart_items:
        total_price += item["price"] * item["quantity"]

    return render_template(
        "shop/cart.html", cart_items=cart_items, total_price=total_price
    )


@bp.route("/checkout", methods=("GET", "POST"))
def checkout():
    if g.user == None:
        return render_template("error.html")

    """Shows cart info."""
    # checks if user has a cart open
    cart = (
        get_db()
        .execute(
            "SELECT * FROM cart WHERE user_id = ? AND cart_status = 'active'",
            (g.user["id"],),
        )
        .fetchone()
    )

    # if the user doens't have a cart open, or its empty, go back to the shop
    if cart is None or cart["total"] == 0:
        return render_template("error.html")

    if request.method == "POST":
        
        if(test_password(request.form["password"])):
            
            # change cart status to 'closed'
            get_db().execute(
                "UPDATE cart SET cart_status = 'closed' WHERE id = ?", (cart["id"],)
            )
            get_db().commit()

            delivery_address = request.form["shipping_address"]
            # create order
            get_db().execute(
                "INSERT INTO orders (cart_id, delivery_address) VALUES (?,?)",
                (cart["id"], delivery_address),
            )
            get_db().commit()

            # get cart items
            cart_items = get_db().execute(
                "SELECT product_id, quantity FROM cart_item WHERE cart_id = ?",
                (cart["id"],)
            ).fetchall()
            
            # Decrement product quantities in the database
            for item in cart_items:
                product_id = item["product_id"]
                cart_quantity = item["quantity"]

                # Update the product quantity in the database
                product = get_db().execute(
                    "SELECT quantity FROM products WHERE id = ?", (product_id,)
                ).fetchone()

                if product is not None:
                    stock_quantity = product["quantity"]
                    new_quantity = stock_quantity - cart_quantity

                    if new_quantity < 0:
                        new_quantity = 0

                    get_db().execute(
                        "UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id)
                    )
                    get_db().commit()
        else:
            flash("Wrong password")
            return redirect(url_for("shop.checkout"))

        return redirect(url_for("shop.index"))

    return render_template("shop/checkout.html")


def sanitize_input(input_str):
    """
    Sanitize user input by escaping special characters that might be used for HTML tags.
    """
    if input_str is None:
        return None

    character_map = {
        '<': '&lt;',
        '>': '&gt;'
    }

    # Replace special characters with their corresponding HTML entities
    sanitized_str = ''.join(character_map.get(c, c) for c in input_str)

    return sanitized_str


@bp.route("/<int:id>/createreview", methods=("GET", "POST"))
@login_required
def createreview(id):
    db = get_db()

    product_name = db.execute(
        "SELECT productname FROM products WHERE id = ?", (id,)
    ).fetchone()
    
    if product_name is not None:

        """Adds review to product"""
        if request.method == "POST":
            title = request.form["title"]
            review = request.form["review"]
            rating = int(request.form["rating"])

            sanitized_review = sanitize_input(review)

            error = None

            if not title:
                error = "Review is required."
            if not rating:
                error = "Rating is required."
            if error is not None:
                flash(error)
            else:
                db.execute(
                    "INSERT INTO reviews (author_id, author_username, title, review, rating, product_id) VALUES (?, ?, ?, ?, ?, ?)",
                    (g.user["id"], g.user["username"], title, sanitized_review, rating, id),
                )
                db.commit()

                product_name = db.execute(
                    "SELECT productname FROM products WHERE id = ?", (id,)
                ).fetchone()

                return redirect(url_for("shop.productinfo", name=product_name[0]))

        return render_template("shop/createReview.html")
    else:
        return render_template("error.html")
