from flask import render_template, url_for, flash, redirect
from app.models import Post, User
from app.form import RegistrationForm, LoginForm
from app import app

posts = [
    {
        "title": "First Blog Post",
        "author": "Jane Foster",
        "date_posted": "13 May, 2020",
        "content": "This is first blog post in this blog"
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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Acount created for {form.username.data}!", "success")
        return redirect(url_for('home'))
    return render_template("register.html", title="Register an Account", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash("You have been logged in!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login Failed! Please check your Email and Password", 'danger')
    return render_template("login.html", title="User Login", form=form)
