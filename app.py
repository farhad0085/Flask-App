from flask import Flask, render_template, url_for, flash, redirect
from form import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "ac24802fb9a07239ef77af1ac2995fa4"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

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

if __name__ == "__main__":
    app.run(debug=True)
