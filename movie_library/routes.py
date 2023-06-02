from flask import render_template, session, request, redirect, url_for, flash
from movie_library import app, db
from movie_library.forms import MovieForm, ExtendedMovieForm, RegisterForm, LoginForm
from movie_library.models import Movie, User
import datetime as dt
import functools

with app.app_context():
    db.create_all()

def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for("login"))
        return route(*args, **kwargs)

    return route_wrapper

@app.route("/")
@login_required
def index():
    user = User.query.filter_by(email=session['email']).first()
    if user and user.movies:
        movies = [movie for movie in user.movies]
        print(movies)
    else:
        movies = []
    return render_template("index.html", title="Movies Watchlist", movies_data=movies)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if session.get("email"):
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        session['email'] = user.email
        flash("User registered successfully", "success")

        return redirect(url_for('login'))

    return render_template("register.html", title="Movies-Watchlist | Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('email'):
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user_data = User.query.filter_by(email=form.email.data).first()
        
        if not user_data:
            flash("Login credentials not correct", category="danger")
            return redirect(url_for('login'))
        if user_data.check_password_correction(attempted_password=form.password.data):
        
            session["user_id"] = user_data.id
            session["email"] = user_data.email

            return redirect(url_for('index'))

        flash("Login credentials incorrent", category='danger')

    return render_template("login.html", title="Movie Watchlist | Login", form=form)

@app.route('/logout')
def logout():
    current_theme = session.get('theme')
    session.clear()
    session['theme'] = current_theme
    return redirect(url_for('login'))


@app.get('/movie/<string:_id>')
def movie(_id: int):
    movie = Movie.query.filter_by(id=_id).first()
    return render_template("movie_details.html", movie=movie)

@app.get("/movie/<string:_id>/rate")
@login_required
def rate_movie(_id: int):
    rating = int(request.args.get('rating'))
    movie = Movie.query.filter_by(id=_id).first()
    movie.rating = rating
    db.session.commit()

    return redirect(url_for('movie', _id=_id))

@app.get('/movie/<string:_id>/watch')
@login_required
def watch_today(_id):
    movie = Movie.query.filter_by(id=_id).first()
    before_format = dt.datetime.today()
    formatted_date = before_format.strftime('%d %b %Y')
    movie.last_watched = formatted_date
    db.session.commit()

    return redirect(url_for('movie', _id=_id))


@app.route('/add', methods=["GET", "POST"])
@login_required
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        db.create_all()
        movie = Movie(title=form.title.data, director=form.director.data, year=form.year.data)
        db.session.add(movie)
        
        movie.owner = User.query.filter_by(id=session['user_id']).first().id
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('new_movie.html', title="Movies Watchlist | Add Movie", form=form)


@app.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == 'dark':
        session['theme'] = "light"
    else:
        session['theme'] = 'dark'
    return redirect(request.args.get("current_page"))


@app.route('/edit/<string:_id>', methods=["GET","POST"])
@login_required
def edit_movie(_id):
    movie = Movie.query.filter_by(id=_id).first()
    form = ExtendedMovieForm(obj=movie)            # pre-population
    if form.validate_on_submit():
        movie.title=form.title.data
        movie.description=form.description.data
        movie.year=form.year.data
        movie.favourite_actor=form.favourite_actor.data
        movie.tags=form.tags.data
        movie.description=form.description.data
        movie.video_link=form.video_link.data

        db.session.commit()
        return redirect(url_for('movie', _id=movie.id))
    return render_template('movie_form.html', movie=movie, form=form)


