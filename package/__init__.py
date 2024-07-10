from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
loginManager = LoginManager()
# loginManager.login_view = "users.login"

mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER")
    app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS")
        
    db.init_app(app)
    migrate = Migrate(app, db)
    bcrypt.init_app(app)
    loginManager.init_app(app)
    # loginManager.login_view = "users.login"

    mail.init_app(app)
    from package.users.routes import users
    from package.posts.routes import posts
    from package.main.routes import main
    from package.comments.routes import comment
    from package.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(comment)

    return app