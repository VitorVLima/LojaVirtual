from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_login import LoginManager, login_manager
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SJBKJABAHB'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#configurações de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'clienteLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u"FAZER LOGIN PRIMEIRO"

#configurações para carregamento de imagens 
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

from loja.admin import routes
from loja.produtos import routes
from loja.carrinho import carrinhos
from loja.clientes import routes












