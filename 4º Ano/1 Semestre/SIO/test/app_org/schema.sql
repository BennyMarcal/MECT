-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS cart;
DROP TABLE IF EXISTS cart_item;
DROP TABLE IF EXISTS orders;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT,
  password TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'normal'
);

CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  productname TEXT UNIQUE NOT NULL,
  price INTEGER NOT NULL,
  info TEXT,
  quantity INTEGER NOT NULL,
  category TEXT,
  img TEXT
);

CREATE TABLE reviews (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER NOT NULL,
  author_id INTEGER NOT NULL,
  author_username TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  rating INTEGER NOT NULL,
  review TEXT,
  FOREIGN KEY (product_id) REFERENCES products (id),
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (author_username) REFERENCES user (username)
);


CREATE TABLE cart (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  total INTEGER NOT NULL DEFAULT 0,
  cart_status TEXT NOT NULL DEFAULT 'active',
  date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE cart_item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cart_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products (id),
  FOREIGN KEY (cart_id) REFERENCES cart (id)
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cart_id INTEGER NOT NULL,
  delivery_address INTEGER NOT NULL,
  date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cart_id) REFERENCES cart (id)
);


INSERT INTO products  (productname, price, info, quantity, category, img) VALUES 
  ('ECT Hoodie', 30, 'Cool hoodie', 30, 'clothing', 'hoodie.jpeg'),
  ('ECT Key Chain', 2.99, 'Cool key chain', 50, 'others', 'key_chain.jpeg'),
  ('Notebook', 5.99, 'Good quality notebook to take notes of everything you need', 50, 'office supplies', 'notebook.jpeg'),
  ('ECT Pen', 1.99, 'Great quality pen', 80, 'office supplies', 'pen.jpeg'),
  ('T-Shirt', 19.99, 'Plain white T-Shirt', 60, 'clothing', 'tshirt.jpg'),
  ('Jacket', 39.99, 'Blue jacket', 40, 'clothing', 'casaco.jpg'),
  ('Mug', 9.99, 'White mug', 90, 'others', 'caneca.png');
