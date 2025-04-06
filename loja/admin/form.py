from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import Email, DataRequired
from flask_wtf.file import FileAllowed, FileRequired, FileField,ValidationError
from flask_wtf import FlaskForm

class RegistrationForm(FlaskForm):
    nome = StringField('Nome Completo', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
    
    # Definindo o campo senha primeiro para permitir a comparação
    senha = PasswordField('Digite sua Senha', [
        validators.DataRequired(message='A senha não pode estar vazia'), 
        validators.Length(min=6, message='A senha deve ter no mínimo 6 caracteres')])
    
    # O campo confirmacao deve vir depois da senha para a comparação funcionar corretamente
    confirmacao = PasswordField('Confirmar sua Senha', [
        validators.DataRequired(message='Por favor, confirme sua senha'),
        validators.EqualTo('senha', message='Sua senha e confirmação não são iguais')])
    
    def validate_username(self, username):
        if RegistrationForm.query.filter_by(username = username.data).first():
            raise ValidationError("Este usuário ja existe no sistema")
    def validate_email(self, email):
        if RegistrationForm.query.filter_by(email = email.data).first():
            raise ValidationError("Este Email ja existe no sistema")
    

class LoginFormulario(FlaskForm):
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
    
    # Definindo o campo senha primeiro para permitir a comparação
    senha = PasswordField('Digite sua Senha', [
        validators.DataRequired(message='A senha não pode estar vazia')])

    