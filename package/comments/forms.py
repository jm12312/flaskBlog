from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    content = StringField("Enter your comments", validators=[DataRequired()])
    send = SubmitField("Send")