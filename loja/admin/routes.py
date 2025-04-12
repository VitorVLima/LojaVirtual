from flask import render_template, session, request, url_for, flash, redirect
from loja import app, db, bcrypt
from .form import RegistrationForm, LoginFormulario
import os
from .models import User
from loja.produtos.models import Addproduto, Marca, Categoria
from loja.admin.models import User
from flask_login import login_required, current_user , login_user, logout_user


@app.route("/admin")
@login_required
def admin():
    flash(f'Conectado como administrador ','success')
    produtos = Addproduto.query.all()
    return render_template('admin/index.html', title='Pagina Administrativa', produtos=produtos)

@app.route("/marcas")
@login_required
def marcas():
    flash(f'Conectado como administrador ','success')
    marcas = Marca.query.order_by(Marca.id.desc()).all()
    return render_template('admin/marcas.html', title='Pagina Fabricantes', marcas = marcas)

@app.route("/categoria")
@login_required
def categoria():
    flash(f'Conectado como administrador ','success')
    categorias = Categoria.query.order_by(Categoria.id.desc()).all()
    return render_template('admin/categorias.html', title='Pagina Categorias', categorias = categorias)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrationForm()
    
    if request.method == 'POST':
        if form.validate():
            # Apenas então gera o hash da senha
            hash_password = bcrypt.generate_password_hash(form.senha.data)
            
            user = User(nome=form.nome.data, username=form.username.data, email=form.email.data, senha=hash_password)
            db.session.add(user)
            db.session.commit()  # O método correto é `commit()` (não `db.commit()`)
            flash(f'Obrigado {form.nome.data} por registrar','success')
            return redirect(url_for('login'))
        else:
            # Caso o formulário não seja válido, exibe as mensagens de erro
            flash('Por favor, corrija os erros no formulário.')
            return redirect(url_for('registrar'))

    return render_template('admin/registrar.html', form=form, title='Página de Registros')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginFormulario()
    if request.method == 'POST':
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.senha, form.senha.data):
            login_user(user)
            flash(f'Olá novamente {user.username}', 'success')
            return redirect(url_for('admin'))
        else:
            flash(f'NAO FOI POSSIVEL ACESSAR O SISTEMA','danger')
            return  redirect(url_for('login'))
    return render_template('admin/login.html',form = form, title='Pagina Login')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
