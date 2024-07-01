import os
from flask_login import current_user
from flask import url_for, current_app
import secrets
from PIL import Image
from package import mail
from flask_mail import Message

def save_img(img):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(img.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_name)
    if current_user.image and current_user.image != "default.jpg":
        cwd = os.getcwd()
        cwd = cwd.replace("\\", "/")
        os.remove(cwd+"/package/static/profile_pics/"+ current_user.image)
    size = (200, 200)
    i = Image.open(img)
    i.thumbnail(size)
    i.save(picture_path)
    return picture_name


def send_reset(user):
    token = user.get_reset_token()
    msg = Message("Password reset request", sender="noreply@demo.com", recipients=[user.email])
    msg.body = f"""To reset your password visit the following link: {url_for("users.reset_password", token=token, _external=True)} 
If you did not make this request. Simply Ignore this message."""
    mail.send(msg)