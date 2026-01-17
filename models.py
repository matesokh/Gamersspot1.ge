from datetime import datetime
from ext import db, login_manager
from flask_login import UserMixin
 

class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(5), nullable=False)
    description = db.Column(db.String, nullable=False)
    download_link = db.Column(db.String, nullable=False)
    image = db.Column(db.String, default="default_img.jpg")


class Tournament(db.Model):
    __tablename__ = "tournaments"
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String, nullable=False)
    game_type = db.Column(db.String, nullable=False)    
    max_players = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=False)
    image = db.Column(db.String, default="default_tournament.jpg")
    

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='comments')

class User(db.Model, UserMixin):

    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default="user")


    def __init__(self, username, email, password, role="Guest"):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 