from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from package import db
from package.posts.forms import PostForm
from package.models import Post, Like

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


@posts.route("/post/<int:id>", methods=["GET", "POST"])
def post(id):
    post = Post.query.get_or_404(id)
    like_post = Like.query.filter_by(p_id=id).all()
    return render_template("post.html", title=post.title, post=post, like_post=len(like_post))

@posts.route("/post/<int:id>/like", methods=["POST"])
@login_required
def like_post(id):
    like = Like.query.filter_by(u_id=current_user.id, p_id=id).first()
    # print(Like.query.filter_by(u_id=current_user.id, p_id=id).all())
    if like:
        db.session.delete(like)
        db.session.commit()
    else:
        new_like = Like(u_id=current_user.id, p_id=id)
        db.session.add(new_like)
        db.session.commit()
    return redirect(url_for('posts.post', id=id))



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
