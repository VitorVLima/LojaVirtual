from flask import redirect, render_template, url_for, flash, request, session, current_app
from .form import Addprodutos
from loja import db, app, photos
from .models import Marca, Categoria, Addproduto
import secrets, os

@app.route("/")
def home():
    produtos = Addproduto.query.filter(Addproduto.stock>0)
    marcas = Marca.query.join(Addproduto,(Marca.id == Addproduto.marca_id)).all()
    categorias = Categoria.query.join(Addproduto,(Categoria.id == Addproduto.categoria_id)).all()
    return render_template('produtos/index.html', produtos = produtos, marcas = marcas, categorias=categorias)

@app.route('/marca/<int:id>', methods=['GET','POST'])
def get_marca(id):
    marca = Addproduto.query.filter_by(marca_id=id).all()
    marcas = Marca.query.join(Addproduto,(Marca.id == Addproduto.marca_id)).all()
    categorias = Categoria.query.join(Addproduto,(Categoria.id == Addproduto.categoria_id)).all()
    return render_template('/produtos/index.html', marca = marca, marcas = marcas, categorias = categorias)

@app.route('/categoria/<int:id>', methods=['GET','POST'])
def get_categoria(id):
    categoria = Addproduto.query.filter_by(categoria_id=id).all()
    categorias = Categoria.query.join(Addproduto,(Categoria.id == Addproduto.categoria_id)).all()
    marcas = Marca.query.join(Addproduto,(Marca.id == Addproduto.marca_id)).all()
    return render_template('/produtos/index.html', categoria = categoria, categorias = categorias, marcas = marcas)

@app.route('/addmarca', methods=['GET','POST'])
def addmarca():
    if 'email' not in session:
        flash(f'Por Favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        getmarca = request.form.get('marca')
        marca = Marca(name=getmarca)
        db.session.add(marca)
        db.session.commit()
        flash(f'A marca {getmarca} foi cadastrada com sucesso', 'success')
        return redirect(url_for('marcas'))
    return render_template('/produtos/addmarca.html',marcas = 'marcas')

@app.route('/updatemarca/<int:id>', methods=['GET','POST'])
def updatemarca(id):
    if 'email' not in session:
        flash(f'Por Favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))
    
    updatemarca = Marca.query.get_or_404(id)
    marca = request.form.get('marca')
    if request.method == 'POST':
        updatemarca.name = marca
        flash(f'Seu fabricante foi atualizado com sucesso', 'danger')
        db.session.commit()
        return redirect(url_for('marcas'))

    return render_template('/produtos/updatemarca.html',title = 'Atualizar Fabricante', updatemarca = updatemarca)

@app.route('/deletemarca/<int:id>', methods=['POST'])
def deletemarca(id):
    if 'email' not in session:
        flash(f'Por Favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))

    marca = Marca.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(marca)
        db.session.commit()
        flash(f'A Marca {marca.name} foi deletada com sucesso', 'success')
        return redirect(url_for('marcas'))
    flash(f'Não foi possível deletar a marca {marca.name}', 'danger')
    return redirect(url_for('marcas'))


@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash(f'Por Favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        getmarca = request.form.get('categoria')
        cat = Categoria(name=getmarca)
        db.session.add(cat)
        db.session.commit()
        flash(f'A Categoria {getmarca} foi cadastrada com sucesso', 'success')
        return redirect(url_for('categoria'))
    return render_template('/produtos/addmarca.html')

@app.route('/updatecat/<int:id>', methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Por Favor fazer seu login no sistema', 'success')
        return redirect(url_for('login'))
    
    updatecat = Categoria.query.get_or_404(id)
    categoria = request.form.get('categoria')
    if request.method == 'POST':
        updatecat.name = categoria
        flash(f'Sua Categoria foi atualizada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('categoria'))

    return render_template('/produtos/updatemarca.html',title = 'Atualizar Categoria', updatecat = updatecat)

@app.route('/deletecat/<int:id>', methods=['POST'])
def deletecat(id):
    if 'email' not in session:
        flash(f'Por Favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))

    categoria = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        try:
            db.session.delete(categoria)
            db.session.commit()
            flash(f'A Categoria {categoria.name} foi deletada com sucesso', 'success')
            return redirect(url_for('categoria'))
        except:
            flash(f'Erro ao tentar excluir cateforia', 'danger')
            return redirect(url_for('categoria'))
    flash(f'Não foi possivel deletar a catetoria {categoria.name}', 'danger')
    return redirect(url_for('categoria'))


@app.route('/addproduto', methods=['GET','POST'])
def addproduto():
    if 'email' not in session:
        flash(f'Por Favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))
    
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    form = Addprodutos(request.form)
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        marca = request.form.get('marca')
        categoria = request.form.get('categoria')
        image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
        image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
        image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")

        addpro = Addproduto(name=name,price=price,discount=discount,stock=stock,colors=colors,desc=desc,marca_id=marca,categoria_id=categoria,image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        db.session.commit()
        flash(f'O produto {name} foi cadastrado com sucesso', 'success')
        return redirect(url_for('admin'))


    return render_template('/produtos/addproduto.html', title = 'Cadastrar Produto', form = form, marcas = marcas, categorias = categorias)

@app.route('/updateproduto/<int:id>', methods=['GET','POST'])
def updateproduto(id):
    if 'email' not in session:
        flash(f'Por Favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))
    
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    produto = Addproduto.query.get_or_404(id)
    marca = request.form.get('marca')
    categoria = request.form.get('categoria')
    form = Addprodutos(request.form)

    if request.method == 'POST':
        produto.name =form.name.data
        produto.price = form.price.data 
        produto.desc = form.discription.data 

        produto.marca_id = marca
        produto.categoria_id = categoria

        produto.stock = form.stock.data 
        produto.colors = form.colors.data 
        produto.discount = form.discount.data 

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + produto.image_1))
                produto.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
            except:
                produto.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
        
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + produto.image_2))
                produto.image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
            except:
                produto.image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
        
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + produto.image_3))
                produto.image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
            except:
                produto.image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")

        

        db.session.commit()
        flash(f'Produto foi atualizado com sucesso', 'success')
        return redirect('/admin')
        

    form.name.data = produto.name
    form.price.data = produto.price
    form.discription.data = produto.desc
    form.stock.data = produto.stock
    form.colors.data = produto.colors
    form.discount.data = produto.discount
    
    


    return render_template('/produtos/updateproduto.html',title = 'Atualizar Produtos', form = form, marcas = marcas, categorias = categorias, produto = produto)

@app.route('/deleteproduto/<int:id>', methods=['POST'])
def deleteproduto(id):
    if 'email' not in session:
        flash(f'Por Favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))

    produto = Addproduto.query.get_or_404(id)
    if request.method == 'POST':
        try:
            if produto.image_1:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + produto.image_1))
            if produto.image_2:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + produto.image_2))
            if produto.image_3:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + produto.image_3))
        except Exception as e:
            print(e)
        db.session.delete(produto)
        db.session.commit()
        flash(f'O produto {produto.name} foi deletado com sucesso', 'success')
        return redirect(url_for('admin'))
    flash(f'Não foi possivel deletar o produto {produto.name}', 'danger')
    return redirect(url_for('admin'))