from flask import render_template, redirect, url_for
from forms import RegisterForm
from forms import loginform, AddGameForm, TournamentForm 
from forms import CommentForm
from models import Comment, Tournament, User, Game
import os 
from ext import app, db
from flask import flash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, current_user, login_required


profiles = [
    
]


products = []

role=""
 


@app.route("/")
def home ():
    return render_template("index.html", role=role)

@app.route("/aboutus")
def aboutus():
    return render_template("AboutUs.html", role=role)


@app.route("/contact")
def contactus():    
    return render_template("contact.html", role=role)

@app.route("/tournaments")
@login_required
def tournaments():
    tournaments = Tournament.query.all()
    return render_template("tournaments.html", role=role, tournaments=tournaments)   


@app.route("/login" , methods=["GET", "POST"])
def login():
    form=loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('You successfully authorized', category='success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template("signin.html", form=form) 


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))


@app.route("/games")
def games():
    games = Game.query.all()
    return render_template("games.html", games=games, role=role)


@app.route("/signup", methods=["POST","GET"])
def signin():
    form = RegisterForm()
    if form.validate_on_submit():
       existing_user = User.query.filter_by(username=form.username.data).first()
       if existing_user:
           flash("Username already exists. Please choose a different username.", category='error')
           return render_template("signin.html", form=form)

       new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)

       db.session.add(new_user)
       db.session.commit()

       flash("Registration successful! Please log in.")
       return redirect("/login")
    return render_template("singup.html", form=form)
   


@app.route("/add-game", methods=["GET", "POST"])
@login_required
def add_game():
    form = AddGameForm()

    if form.validate_on_submit():
        image_file = form.image.data
        filename = None
        if image_file:
            filename = secure_filename(image_file.filename)
            upload_dir = os.path.join('static', 'images')
            os.makedirs(upload_dir, exist_ok=True)
            image_file.save(os.path.join(upload_dir, filename))

        new_game = Game(
            title=form.title.data,
            description=form.description.data,
            download_link=form.download_link.data,
            image=filename or 'default_img.jpg'
            
        )

        db.session.add(new_game)
        db.session.commit()

        return redirect(url_for("games"))
    return render_template("products.html", form=form)

@app.route("/add-tournament", methods=["GET", "POST"])
@login_required
def add_tournament():
    form = TournamentForm()
    if form.validate_on_submit():
       image_file = form.image.data
       filename = None  
       if image_file:
              filename = secure_filename(image_file.filename)
              upload_dir = os.path.join('static', 'images')
              os.makedirs(upload_dir, exist_ok=True)
              image_file.save(os.path.join(upload_dir, filename))
       new_tournament = Tournament(
            game=form.game.data,
            game_type=form.game_type.data,
            max_players=form.max_players.data,
            date=form.date.data,
            image=filename or 'default_tournament.jpg'
        )
       db.session.add(new_tournament)
       db.session.commit() 
       return redirect(url_for("tournaments"))
    return render_template("addtournaments.html", form=form)   

@app.route("/profiles/<int:profile_id>")
def profile(profile_id):
     return render_template("profiles.html", user=profiles[profile_id])

@app.route("/delete-game/<int:game_id>", methods=["POST"])
@login_required
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)

    Comment.query.filter_by(product_id=game.id).delete()
    db.session.delete(game)
    db.session.commit()

    flash("Game deleted successfully")
    return redirect(url_for("games"))

@app.route("/delete-tournament/<int:tournament_id>", methods=["POST"])
@login_required
def delete_tournament(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)

    Comment.query.filter_by(product_id=tournament.id).delete()
    db.session.delete(tournament)
    db.session.commit()

    flash("Tournament deleted successfully")
    return redirect(url_for("tournaments"))


@app.route("/navbar")
def navbar():
    return render_template("navbar.html", role=role)


@app.route('/games/<int:game_id>', methods=['GET', 'POST'])
@login_required
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
    comments = Comment.query.filter_by(product_id=game.id).all()
    form = CommentForm()

    if form.validate_on_submit():
        new_comment = Comment(
            text=form.text.data,
            product_id=game.id,
            user_id=current_user.id
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("game_detail", game_id=game.id))
    
    return render_template('detail.html', game=game, comments=comments, role=current_user.role, form=form)

@app.route('/comments/delete/<int:comment_id>/<int:game_id>', methods=['POST'])
@login_required
def delete_comment(comment_id, game_id):
    if current_user.role != "Admin":
        flash("You are not authorized to delete comments.", "danger")
        return redirect(url_for("game_detail", game_id=game_id))

    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted successfully.", "success")
    return redirect(url_for("game_detail", game_id=game_id))