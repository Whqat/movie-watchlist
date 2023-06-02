from decouple import config
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


load_dotenv()



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mwl.db"
app.secret_key = config("SECRET_KEY")
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from movie_library import routes
    
