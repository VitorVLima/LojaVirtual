from loja import db, app, login_manager
from datetime import datetime
from flask_login import UserMixin
import json

class JsonEcodedDirect(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
        
    def process_ressult_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


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
        return '<CadastrarCliente %r>' % self.name
    
class ClientePedido(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    notaFiscal = db.Column(db.String(50), unique = True, nullable = False)
    status = db.Column(db.String(50), default='pendente', nullable = False )
    cliente_id = db.Column(db.String(50), unique = False, nullable = False )
    data_criado= db.Column(db.DateTime, default=datetime.utcnow, nullable = False)
    pedido = db.Column(JsonEcodedDirect)

    def __repr__(self):
        return '<ClientePedido %r>' % self.notaFiscal
   
    
with app.app_context():
    db.create_all()



