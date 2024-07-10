from flask import Blueprint, request, render_template, redirect, url_for
from package.models import Post, Like, Comment
from package import db

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    pg = request.args.get("page", 1, type=int)
    val = request.args.get("val", 1 , type=int)
    posts = get_order(val).paginate(per_page=5, page=pg)
    return render_template("home.html", posts=posts, val=val)

@main.route("/home/order", methods=["POST"])
def post_order():
    print("Entered")
    val = int(request.form.get("order"))

    return redirect(url_for("main.home", val=val))

def get_order(val):
    if val==1 or val==0:
        posts = Post.query.order_by(Post.date_posted.desc())
    elif val==2:
        posts = Post.query.order_by(Post.date_posted)
    elif val==3:
        posts = Post.query.outerjoin(Like).group_by(Post.id).order_by(db.func.count(Like.id).desc())
    elif val==4:
        posts = Post.query.outerjoin(Comment).group_by(Post.id).order_by(db.func.count(Comment.id).desc())

    return posts


@main.route("/about")
def about():
    return render_template("about.html", title="Joshua")

