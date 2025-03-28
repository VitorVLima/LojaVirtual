from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_msearch import Search
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os

# Caminho base
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# Configurações do Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SJBKJABAHB'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)

# Inicializa o Flask-Bcrypt
bcrypt = Bcrypt(app)

# Inicializa o Upload de Imagens
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

# Inicializa o Flask-MSearch após o SQLAlchemy
# Inicializa o Flask-MSearch dentro do contexto do app

search = Search()
search.init_app(app)


# Importações
from loja.admin import routes
from loja.produtos import routes
from loja.carrinho import carrinhos









