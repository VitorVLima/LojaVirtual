from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField

class Addprodutos(FlaskForm):
    name = StringField('Nome: ', [validators.DataRequired()])
    price = DecimalField('Preco: ', [validators.DataRequired()])
    stock = IntegerField('Estoque: ', [validators.DataRequired()])
    discount = IntegerField('Desconto: ', [validators.DataRequired()])
    discription = TextAreaField('Descricao: ', [validators.DataRequired()])
    colors = TextAreaField('Cor: ', [validators.DataRequired()])

    image_1 = FileField('Image 1: ', validators=[FileAllowed(['jpg','png', 'gif', 'jpeg', 'webp'])])
    image_2 = FileField('Image 2: ', validators=[FileAllowed(['jpg','png', 'gif', 'jpeg', 'webp'])])
    image_3 = FileField('Image 3: ', validators=[FileAllowed(['jpg','png', 'gif', 'jpeg', 'webp'])])