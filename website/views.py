from . import app, db
from flask import render_template, flash, redirect, url_for
from .forms import RegisterForm, LoginForm, ChangePasswordForm
from .models import User, Message
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/")
@login_required
def home():
    return render_template("home.html", name=current_user.login) #*

@app.route("/secret")
@login_required
def secret():
    return "hej ;)"

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if not user:
            flash("Nie znaleziono uzytkownika", category="danger")
        elif not check_password_hash(user.password, form.password.data):
            flash("Niepoprawne haslo", category="danger")
        else:
            login_user(user)
            flash("Zalogowano", category="success")
            return redirect(url_for("home"))
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(login=form.login.data, password=generate_password_hash(form.password1.data, method="sha512"))
        db.session.add(user)
        db.session.commit()
        flash("Udało się", category="success")
        return redirect(url_for("login"))
    else:
        flash("Pojawil sie jakis blad (doimplementowac pozniej..)", category="danger")
    return render_template("register.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/messages/<int:user_id>")
@login_required
def messages(user_id):
    user = User.query.get(user_id)
    if not user:
        return "Not found", 404
    msgs = []
    msgs += Message.query.filter_by(user_id_from=current_user.id, user_id_to=user_id)
    msgs += Message.query.filter_by(user_id_from=user_id, user_id_to=current_user.id)
    msgs.sort(key=lambda m: m.date_created)
    return render_template("messages.html", messages=msgs, user_to=user, users=User.query.all())

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password, form.old_password.data):
            current_user.password = generate_password_hash(form.new_password.data, method="sha512")
            db.session.commit()
            flash("Password changed!", category="success")
        else:
            flash("Invalid old password", category="danger")
    return render_template("settings.html", form=form)
