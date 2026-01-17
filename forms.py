from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField,SubmitField,FileField,IntegerField

from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired





class RegisterForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = EmailField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), Length(min=8, max=16)])
    submit = SubmitField("Register")


class AddGameForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    image = FileField("Image filename", validators=[DataRequired()])
    download_link = StringField("Download Link", validators=[DataRequired()])
    submit = SubmitField("Add Game")

class loginform(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), Length(min=8, max=16)])
    submit = SubmitField("Login")

class TournamentForm(FlaskForm):
   game = StringField("Game", validators=[DataRequired()])
   game_type=StringField("Game Type", validators=[DataRequired()])
   max_players = IntegerField("Max Players", validators=[DataRequired()])
   date=StringField("Date", validators=[DataRequired()])
   image = FileField("Image filename", validators=[DataRequired()])
   submit = SubmitField("Create Tournament")
   

class CommentForm(FlaskForm):
    text = StringField("Add a comment", validators=[DataRequired()])
    submit = SubmitField("Post Comment")

    
    
