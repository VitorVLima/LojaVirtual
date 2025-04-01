from flask import redirect, render_template, url_for, flash, request, session, current_app, make_response
from loja.clientes.forms import CadastroClienteForm, ClienteLoginForm
from loja import db, app, bcrypt, login_manager
from loja.produtos.models import Marca, Categoria, Addproduto
import secrets, os
from loja.clientes.models import CadastrarCliente, ClientePedido
from flask_login import login_required, current_user , login_user, logout_user
import json
import pdfkit
import stripe

stripe.api_key = 'sk_test_51R89TcGbhM6idagM9uLXceTIkN6dDf8vj9MZZ8NElwKigH9bmkDA6EItTqv9NdNIF9mjjCkZoYBEkcEMqWkGAgJL00Tm8L7DgT'

@app.route('/obrigado')
def obrigado():
    return render_template('cliente/obrigado.html', title = "Pagamento Aceito")

@app.route('/pagamento', methods=['POST'])
@login_required
def pagamento():
    notaFiscal = request.form.get('invoice')
    amount = int(float(request.form.get('amount')))
    customer = stripe.Customer.create(
    email=request.form['stripeEmail'],
    source= request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
    customer=customer.id,
    description='Loja_flask',
    amount=amount,
    currency='brl',
    )
    cliente_pedido = ClientePedido.query.filter_by(cliente_id = current_user.id, notaFiscal= notaFiscal).order_by(ClientePedido.id.desc()).first()
    cliente_pedido.status = 'Pago'
    db.session.commit()

    return redirect(url_for('obrigado'))

@app.route('/cliente/cadastrar', methods=['GET','POST'])
def cadastrar_clientes():
    form = CadastroClienteForm()
    if form.validate_on_submit():
        print("Formulário validado com sucesso!") #adicione essa linha.
        hash_password = bcrypt.generate_password_hash(form.password.data)
        cadastrar = CadastrarCliente(name = form.name.data.title(), username = form.username.data, email = form.email.data, password = hash_password, country = form.country.data, state = form.state.data, city= form.city.data, address = form.address.data,contact = form.contact.data, zipcode = form.zipcode.data)
        db.session.add(cadastrar)
        flash(f'Obrigado {form.name.data} pelo seu cadastro', 'success')
        db.session.commit()
        return redirect(url_for('clienteLogin'))
    print(form.errors) #adicione essa linha.
    return render_template('cliente/cliente.html', form = form, title = "Cadastrar Usuário")

@app.route('/cliente/login', methods=[ 'GET', 'POST'])
def clienteLogin():
    form = ClienteLoginForm()
    if form.validate_on_submit():
        user = CadastrarCliente.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Olá novamente {user.username}', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
       
        flash('Usuario ou Senha inválidos', 'danger')
        return redirect(url_for('clienteLogin'))
    
    return render_template('cliente/login.html', form = form, title = "Login Usuário")



@app.route('/cliente/logout')
def cliente_logout():
    logout_user()
    return redirect(url_for('home'))

def atualizarlojaCarro():
    for _key, produto in session['LojainCarrinho'].items():
        session.modified = True
        del produto['image']
        del produto['colors']

    return atualizarlojaCarro


@app.route('/pedido_order')
@login_required
def pedido_order():
    if current_user.is_authenticated:
        cliente_id = current_user.id
        notaFiscal = secrets.token_hex(5)
        atualizarlojaCarro()
        try:
            p_order = ClientePedido(notaFiscal = notaFiscal, cliente_id = cliente_id, pedido = session['LojainCarrinho'])
            db.session.add(p_order)
            db.session.commit()
            session.pop('LojainCarrinho')
            flash('Seu pedido foi registrado com sucesso', 'success')
            return redirect(url_for('pedidos',notaFiscal = notaFiscal))
        except Exception as e:
            print(e)
            flash('Não foi possível processar seu pedido','danger')
            return redirect(url_for('getCart'))
        
@app.route('/pedidos/<notaFiscal>')
@login_required
def pedidos(notaFiscal):
    if current_user.is_authenticated:
        gTotal = 0
        subtotal = 0

        cliente_id = current_user.id
        cliente = CadastrarCliente.query.filter_by(id = cliente_id).first()
        pedidos = ClientePedido.query.filter_by(cliente_id = cliente_id, notaFiscal= notaFiscal).order_by(ClientePedido.id.desc()).first()
        if isinstance(pedidos.pedido, str):
            pedidos.pedido = json.loads(pedidos.pedido)
        
        for _key, produto in pedidos.pedido.items():
            discount = (produto['discount'] / 100) * float(produto['price'])
            subtotal += (float(produto['price']) - discount) * int(produto['quantity'])
        imposto = round(0.06 * subtotal, 2)  # Imposto de 6%
        gTotal = round(subtotal + imposto, 2)
        marcas = Marca.query.join(Addproduto, (Marca.id == Addproduto.marca_id)).all()
        categorias = Categoria.query.join(Addproduto, (Categoria.id == Addproduto.categoria_id)).all()
        # Aparece dados na barra de navegação (marcas e categorias)
    
    else:
        return redirect(url_for('clienteLogin'))
    return render_template('cliente/pedido.html', notaFiscal = notaFiscal, imposto = imposto, subtotal = subtotal, gTotal = gTotal, cliente = cliente, pedidos = pedidos, marcas = marcas, categorias = categorias)

@app.route('/get_pdf/<notaFiscal>', methods=['POST'])
@login_required
def get_pdf(notaFiscal):
    if current_user.is_authenticated:
        gTotal = 0
        subtotal = 0

        cliente_id = current_user.id
        if request.method == 'POST':

            cliente = CadastrarCliente.query.filter_by(id = cliente_id).first()
            pedidos = ClientePedido.query.filter_by(cliente_id = cliente_id, notaFiscal= notaFiscal).order_by(ClientePedido.id.desc()).first()
            if isinstance(pedidos.pedido, str):
                pedidos.pedido = json.loads(pedidos.pedido)
            
            for _key, produto in pedidos.pedido.items():
                discount = (produto['discount'] / 100) * float(produto['price'])
                subtotal += (float(produto['price']) - discount) * int(produto['quantity'])
            imposto = round(0.06 * subtotal, 2)  # Imposto de 6%
            gTotal = round(subtotal + imposto, 2)
            marcas = Marca.query.join(Addproduto, (Marca.id == Addproduto.marca_id)).all()
            categorias = Categoria.query.join(Addproduto, (Categoria.id == Addproduto.categoria_id)).all()
            # Aparece dados na barra de navegação (marcas e categorias)
    
            rendered = render_template('cliente/pdf.html', notaFiscal = notaFiscal, imposto = imposto, subtotal = subtotal, gTotal = gTotal, cliente = cliente, pedidos = pedidos, marcas = marcas, categorias = categorias)
            config = pdfkit.configuration(wkhtmltopdf = 'c:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

            pdf = pdfkit.from_string(rendered, False, configuration=config)
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'attachment;filename=' + notaFiscal +'. pdf'
            return response
    return redirect(url_for('pedidos'))


@app.route('/cliente/historico', methods=['GET', 'POST'])
@login_required
def historico():
    if current_user.is_authenticated:
        cliente_id = current_user.id
        pedidos = ClientePedido.query.filter_by(cliente_id=cliente_id).all()

        # Inicializar a variável subtotal
        subtotal = 0

        # Iterar sobre cada pedido
        for pedido in pedidos:
            if isinstance(pedido.pedido, str):  # Verificar se o pedido é uma string
                pedido.pedido = json.loads(pedido.pedido)

            # Agora que pedido.pedido é um dicionário, podemos processar os itens
            for _key, produto in pedido.pedido.items():
                discount = (produto['discount'] / 100) * float(produto['price'])
                subtotal += (float(produto['price']) - discount) * int(produto['quantity'])

        imposto = round(0.06 * subtotal, 2)  # Imposto de 6%
        gTotal = round(subtotal + imposto, 2)

        marcas = Marca.query.join(Addproduto, (Marca.id == Addproduto.marca_id)).all()
        categorias = Categoria.query.join(Addproduto, (Categoria.id == Addproduto.categoria_id)).all()

    return render_template('cliente/historico.html', pedidos=pedidos, marcas=marcas, categorias=categorias, title='Histórico de pedidos', imposto=imposto, subtotal=subtotal, gTotal=gTotal)

