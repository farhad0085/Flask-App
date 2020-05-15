from flask import render_template, url_for, flash, redirect, request
from app.models import Post, User
from app.form import RegistrationForm, LoginForm, UpdateAccountForm
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image

posts = [
    {
        "title": "First Blog Post",
        "author": "Jane Foster",
        "date_posted": "13 May, 2020",
        "content": "This is first blog post in this blog."
    },
    {
        "title": "Second Blog Post",
        "author": "Thor",
        "date_posted": "13 May, 2020",
        "content": "This is Second blog post in this blog"
    },
    {
        "title": "Third Blog Post",
        "author": "Captain America",
        "date_posted": "13 May, 2020",
        "content": "This is Third blog post in this blog"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts, title="Home")


@app.route("/about")
def about():
    return render_template("about.html", title="About Page")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created", "success")
        return redirect(url_for('login'))
    return render_template("register.html", title="Register an Account", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Failed! Please check your Email and Password", 'danger')
    return render_template("login.html", title="User Login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    # let's convert the file name to a random name so that
    # two images with same name won't override
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # because we don't need file name
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # let's resize our picture
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # let's save the resized image
    i.save(picture_path)
    return picture_fn # return the picture filename so that we can save it to database

@app.route('/account', methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account info has been updated!", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title="User account",
                           image_file=image_file, form=form)