from datetime import datetime
from package import db, loginManager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="author", lazy=True)
    likes = db.relationship("Like", backref="user", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"])
        token = s.dumps({"user_id": self.id})  # Ensure this returns a string
        print(f"Generated Token: {token} (Type: {type(token)})")  # Debugging print statement
        return token

    @staticmethod
    def verify_token(token, expires_sec=1800):
        s= Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token, max_age=expires_sec)["user_id"]
        except:
            return None
        return User.query.get(user_id)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", backref="post", lazy=True)
    likes = db.relationship("Like", backref="post", lazy="dynamic")
    def has_liked(self, user):
        return Like.query.filter_by(u_id=user.id, p_id=self.id).count()>0
    def __repr__(self):
        return f"Post ('{self.title}', '{self.date_posted}')"
    @property
    def like_count(self):
        return self.likes.count()



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    u_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    p_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    p_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    def __repr__(self):
        return f"Like('{self.u_id}', '{self.p_id}')"