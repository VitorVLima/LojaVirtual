from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SJBKJABAHB'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername =="sqlite":
        migrate.init_app(app,db,render_as_batch=True)
    else:
        migrate.init_app(app,db)

#configurações de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'clienteLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u"FAZER LOGIN PRIMEIRO"


from loja.admin import routes
from loja.produtos import routes
from loja.carrinho import carrinhos
from loja.clientes import routes












