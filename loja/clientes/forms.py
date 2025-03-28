from wtforms import Form, IntegerField, FloatField, SubmitField, StringField, TextAreaField, validators, PasswordField
from flask_wtf.file import FileAllowed, FileRequired, FileField,ValidationError
from flask_wtf import FlaskForm
from.models import CadastrarCliente

class CadastroClienteForm(FlaskForm):
    name = StringField('Nome : ')
    username = StringField('Usuario : ', [validators.DataRequired()])
    email = StringField('Email : ', [validators.DataRequired()])
    password = PasswordField('Senha : ', [validators.DataRequired(), validators.EqualTo('confirm', message = 'As duas Senhas não são iguais')])
    confirm = PasswordField('Confirmar Senha : ', [validators.DataRequired()])

    country = StringField('País : ', [validators.DataRequired()])
    state = StringField('Estado : ', [validators.DataRequired()])
    city = StringField('Cidade : ', [validators.DataRequired()])
    contact = StringField('Contato : ', [validators.DataRequired()])
    address = StringField('Endereço : ', [validators.DataRequired()])
    zipcode = StringField('Caixa-Postal : ', [validators.DataRequired()])
    profile = FileField('Perfil', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])

    submit = SubmitField('Cadastrar')

    def validate_username(self, username):
        if CadastrarCliente.query.filter_by(username = username.data).first():
            raise ValidationError("Este usuário ja existe no sistema")
    def validate_email(self, email):
        if CadastrarCliente.query.filter_by(email = email.data).first():
            raise ValidationError("Este Email ja existe no sistema")

class ClienteLoginForm(FlaskForm):
    email = StringField('Email : ', [validators.DataRequired()])
    password = PasswordField('Senha : ', [validators.DataRequired()])