from loja import db, app
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=False, nullable = False)
    username = db.Column(db.String(50), unique=False, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    senha = db.Column(db.String(180), unique=False, nullable = False)
    profile = db.Column(db.String(180), unique=False, nullable = False, default='profile.jpg')

    def __repr__(self):
        return '<User %r>' % self.username
with app.app_context():
    db.create_all()