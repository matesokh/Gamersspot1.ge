from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = "STALINI1945"


os.makedirs(app.instance_path, exist_ok=True)


db_path = os.path.join(app.instance_path, 'database.db')
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
db = SQLAlchemy(app)
