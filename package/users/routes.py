from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import  current_user, login_user, logout_user
from package import db, bcrypt
from package.models import Post, User, Comment, Like
from package.users.forms import RegistrationForm, LoginForm, UpdateForm, RequestResetForm, ResetPasswordForm
from package.users.utils import save_img, send_reset

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password = hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("main.home"))
        else:
            flash("Login unsuccessful", "danger")
            
    return render_template("login.html", title="Login", form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account", methods=["GET", "POST"])
def account():
    if current_user.is_authenticated:
        form = UpdateForm()
        if form.validate_on_submit():
            if form.image.data:
                picture_file_name = save_img(form.image.data)
                current_user.image = picture_file_name
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash("Your Account is updated", "success")
            return redirect(url_for("users.account"))
        elif request.method == "GET":
            form.username.data = current_user.username
            form.email.data = current_user.email
        img = url_for("static", filename="profile_pics/" + current_user.image)
        return render_template("account.html", title="Account", image = img, form=form)
    else:
        return redirect("login")
    

@users.route("/user/<string:username>")
def user_post(username):
    pg = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=3, page=pg)
    comments = Comment.query.filter_by(u_id=user.id).all()
    likes=0
    for post in Post.query.filter_by(author=user).all():
        likes += post.like_count
    return render_template("user_posts.html", posts=posts, user=user, comm = comments, len= len(comments), likes=likes)


@users.route("/request-password", methods=["GET", "POST"])
def request_password():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset(user)
        flash("Email has been sent to your email address", "info")
        return redirect(url_for("users.login"))
    return render_template("request_password.html", form=form, title="Request password")

@users.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_token(token)
    if user is None:
        flash("Invalid or expired token", "warning")
        return redirect(url_for("users.request_password"))
    else:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user.password = hashed_pwd
            db.session.commit()
            flash(f"Your password is updated", "success")
            return redirect(url_for("users.login"))

        return render_template("reset_password.html", form=form, title="Reset password")