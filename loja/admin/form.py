from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import Email, DataRequired

class RegistrationForm(Form):
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
    

class LoginFormulario(Form):
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
    
    # Definindo o campo senha primeiro para permitir a comparação
    senha = PasswordField('Digite sua Senha', [
        validators.DataRequired(message='A senha não pode estar vazia')])

    