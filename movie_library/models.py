from movie_library import db
from datetime import datetime
from movie_library import bcrypt

class Movie(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    director = db.Column(db.String(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)

    series = db.Column(db.Text())
    last_watched = db.Column(db.String())
    favourite_actor = db.Column(db.String())
    rating = db.Column(db.Integer(), default=0)
    tags = db.Column(db.Text())
    description = db.Column(db.Text())
    video_link = db.Column(db.String())
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.title}"

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(length=32), nullable=False)
    movies = db.relation("Movie", backref='owned_user', lazy=True)

    @property                           #PASSWORD HASHING
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
            

    def __repr__(self):
        return f"{self.email}"

