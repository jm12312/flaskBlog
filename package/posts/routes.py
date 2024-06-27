from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from package import db
from package.posts.forms import PostForm
from package.models import Post

posts = Blueprint("posts", __name__)



@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post is created", "success")
        return redirect(url_for("main.home"))
    return render_template("create_post.html", title="New Post", form=form)


@posts.route("/post/<int:id>")
def post(id):
    post = Post.query.get_or_404(id)
    return render_template("post.html", title=post.title, post=post)

@posts.route("/post/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content =  form.content.data 
        db.session.commit()
        flash("Your post is updated", "success")
        return redirect(url_for("posts.post", id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form)


@posts.route("/post/<int:id>/delete", methods=["POST"])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Your post is deleted", "success")
    return redirect(url_for("main.home"))
