# Flask App

This repository is for My Own Flask Web Application

## PIP COMMANDS
```
pip install pillow
pip install flask
pip install flask-login
pip install Flask-SQLAlchemy
pip install Flask-Bcrypt
pip install Flask-WTF
pip install email-validator
pip install flask-mail
```

## INSTALLATION
1. Enable venv
	- open cmd and type `cd venv/scripts`
	- `activate`
2. Run following commands
	```
	cd ../..
	python
	from app import db
	db.create_all()
	exit()
	```
3. Run `python run.py`
4. Navigate to `127.0.0.1:5000` from any browser.