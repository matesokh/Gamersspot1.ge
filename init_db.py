from ext import db, app
from models import User, Game, Tournament, Comment


with app.app_context():
   
    import os
    os.makedirs(app.instance_path, exist_ok=True)

    db.drop_all() 
    db.create_all()


    admin = User(username="admin", password="adminpass", role="Admin", email="admin@example.com")
    db.session.add(admin)
    db.session.commit()