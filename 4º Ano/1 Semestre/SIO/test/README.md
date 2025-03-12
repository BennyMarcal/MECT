# SIO_Proj2

## Description

This project consists in a small online shop that sells memorabilia for
DETI (Department of Electronics, Telecommunications, and Informatics) at the
University of Aveiro. The online shop will feature a variety of items, including
mugs, cups, t-shirts, hoodies, and similar products.

In this assignment, it was asked to evolve the online shop webiste to comply with level 1
Application Security Verification Standard requirements.

## Authors

- Bernardo Marçal - 103236
- Guilherme Alves - 103185
- Luís Leal - 103511
- Rafael Curado - 103199

## Fixed Issues

- 2.1.1 - Verify that user set passwords are at least 12 characters in length (after multiple spaces are combined).

- 2.1.2 - Verify that passwords 64 characters or longer are permitted but may be no longer than 128 characters.

- 2.1.6 - Verify that password change functionality requires the user's current and new password.

- 2.1.8 - Verify that a password strength meter is provided to help users set a stronger password.

- 2.1.12 - Verify that the user can choose to either temporarily view the entire masked password, or temporarily view the last typed character of the password on platforms that do not have this as built-in functionality.

- 3.4.1 - Verify that cookie-based session tokens have the 'Secure' attribute set. 

- 3.4.3 - Verify that cookie-based session tokens utilize the 'SameSite' attribute to limit exposure to cross-site request forgery attacks.

- 3.7.1 - Verify the application ensures a valid login session or requires re-authentication or secondary verification before allowing any sensitive transactions or account modifications.


## Prerequisites

### Install, activate and configure a virtual environment

    $ pip install virtualenv
    $ python<version> -m venv <virtual-environment-name>
    $ source <virtual-environment-name>/bin/activate
    $ pip install -r requirements.txt

## Run

### Original app

    $ flask --app app_org init-db
    $ flask --app app_org run --debug

### Secure app

    $ flask --app app_sec init-db
    $ flask --app app_sec run --debug

### Access to http://127.0.0.1:5000 in a browser

https://flask-session.readthedocs.io/en/latest/index.html

### Changelog

Resolved search query error if done with invalid characters

Resolved password rules not beeing inplied on password change

Resolved error that didn't allow the user to delete an account

Changed so every data related to the user is also removed from the database when deleting an account