from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from os import getenv
from os.path import join
from dotenv import load_dotenv

load_dotenv()
POSTGRES_PASSWORD=getenv("POSTGRES_PASSWORD")
SECRET_KEY=getenv("SECRET_KEY")

app = Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql+psycopg2://postgres:{POSTGRES_PASSWORD}@localhost:5432/flask_blog'
app.config['SQLALCHEMY_ECHO'] = True
app.config['UPLOAD_FOLDER']=join(app.root_path,'static/img')
app.secret_key=SECRET_KEY

db=SQLAlchemy()
db.init_app(app)

migrate=Migrate(app,db)

bcrypt=Bcrypt(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='auth.login'
login_manager.login_message_category='info'

from flaskblog.auth.routes import auth
from flaskblog.post.routes import post
from flaskblog.main.routes import main

app.register_blueprint(auth)
app.register_blueprint(post)
app.register_blueprint(main)