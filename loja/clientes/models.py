from loja import db, app, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def user_carregar(user_id):
    return CadastrarCliente.query.get(user_id)

class CadastrarCliente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = False, nullable = False)
    username = db.Column(db.String(50), unique = True, nullable = False )
    email = db.Column(db.String(50), unique = True, nullable = False )
    password = db.Column(db.String(180), unique=False, nullable = False)
    country = db.Column(db.String(50), unique = False, nullable = False )
    state = db.Column(db.String(50), unique = False, nullable = False )
    city = db.Column(db.String(50), unique = False, nullable = False )
    contact = db.Column(db.String(50), unique = False, nullable = False )
    address = db.Column(db.String(50), unique = False, nullable = False)
    zipcode = db.Column(db.String(50), unique = False, nullable = False)
    profile = db.Column(db.String(50), unique = False, default = 'profile.jpg' )
    data_criado = db.Column(db.DateTime(50), unique = False, nullable = False, default=datetime.utcnow )

    def __repr__(self):
        return '<Cadastrar %r>' % self.name
    
with app.app_context():
    db.create_all()



