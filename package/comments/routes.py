from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from package import db
from package.comments.forms import CommentForm
from package.models import Comment, Post

comment = Blueprint("comment", __name__)

@comment.route("/post/<int:p_id>/comment/new", methods=["GET", "POST"])
@login_required
def new_comment(p_id):
    form = CommentForm()
    post = Post.query.get(p_id)
    if form.validate_on_submit():
        com = Comment(content=form.content.data, author=current_user, post=post)
        db.session.add(com)
        db.session.commit()
        flash("Your comment is posted", "success")
        return redirect(url_for("comment.new_comment", p_id=p_id))
    comm = Comment.query.filter_by(p_id=p_id)
    return render_template("create_comment.html", title="New Comment", form=form, post=post, comment=comm)
