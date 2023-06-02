from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, URLField, PasswordField
from wtforms.validators import InputRequired, NumberRange, Email, Length, EqualTo

class MovieForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    director = StringField("Director", validators=[InputRequired()])
    year = IntegerField('Year', validators=[InputRequired(),
     NumberRange(min=1878, message="Please enter a year in the format YYYY."),
        ],
    )
    submit = SubmitField("Add Movie")


class ExtendedMovieForm(MovieForm):
    favourite_actor = StringField("Favourite Actor")
    tags = StringField("Tags")
    description = TextAreaField("Description")
    video_link = URLField("Video link")

    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(
        min=4, max=32, message="Your password must be between 4 and 32 characters long."
            )
        ])
    confirm_password = PasswordField("Confirm password", validators=[InputRequired(), EqualTo(
        "password", message="This password did not match the one in the password field."
            )
        ])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")