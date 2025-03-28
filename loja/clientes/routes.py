from flask import redirect, render_template, url_for, flash, request, session, current_app
from loja.clientes.forms import CadastroClienteForm, ClienteLoginForm
from loja import db, app, photos, bcrypt, login_manager
from loja.produtos.models import Marca, Categoria, Addproduto
import secrets, os
from loja.clientes.models import CadastrarCliente
from flask_login import login_required, current_user , login_user, logout_user

@app.route('/cliente/cadastrar', methods=['GET','POST'])
def cadastrar_clientes():
    form = CadastroClienteForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        cadastrar = CadastrarCliente(name = form.name.data, username = form.username.data, email = form.email.data, password = hash_password, country = form.country.data, state = form.state.data, city= form.city.data, address = form.address.data,contact = form.contact.data, zipcode = form.zipcode.data)
        db.session.add(cadastrar)
        flash(f'Obrigado {form.name.data} pelo seu cadastro', 'success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('cliente/cliente.html', form = form)

@app.route('/cliente/login', methods=[ 'GET', 'POST'])
def clienteLogin():
    form = ClienteLoginForm()
    if form.validate_on_submit():
        user = CadastrarCliente.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Voce esta logado', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Usuario ou Senha inválidos', 'danger')
        return redirect(url_for('clienteLogin'))
    
    return render_template('cliente/login.html', form = form)


