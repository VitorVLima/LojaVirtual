from flask import redirect, render_template, url_for, flash, request, session, current_app
from .form import Addprodutos
from loja import db, app
from .models import Marca, Categoria, Addproduto
import secrets, os
from unidecode import unidecode
from sqlalchemy import func
from werkzeug.utils import secure_filename 

@app.route("/")
def home():
    #paginacao 
    pagina = request.args.get('pagina',1,type=int)
    produtos = Addproduto.query.filter(Addproduto.stock>0).order_by(Addproduto.id.desc()).paginate(page=pagina,per_page=8)
    #aparecer dados na barra de nav
    marcas = Marca.query.join(Addproduto,(Marca.id == Addproduto.marca_id)).all()
    categorias = Categoria.query.join(Addproduto,(Categoria.id == Addproduto.categoria_id)).all()
    return render_template('produtos/index.html', produtos = produtos, marcas = marcas, categorias=categorias, title = f"Home - Pág {pagina}")

@app.route('/marca/<int:id>', methods=['GET','POST'])
def get_marca(id):
    pagina = request.args.get('pagina',1,type=int)
    get_marca = Marca.query.filter_by(id = id).first_or_404()
    marca = Addproduto.query.filter_by(marca_id=get_marca.id).paginate(page=pagina,per_page=2)
    marcas = Marca.query.join(Addproduto,(Marca.id == Addproduto.marca_id)).all()
    categorias = Categoria.query.join(Addproduto,(Categoria.id == Addproduto.categoria_id)).all()
    return render_template('/produtos/index.html', marca = marca, marcas = marcas, categorias = categorias, get_marca = get_marca, title = f"Produtos {get_marca.name} - Pág {pagina}")

@app.route('/categoria/<int:id>', methods=['GET','POST'])
def get_categoria(id):
    pagina = request.args.get('pagina',1,type=int)
    get_cat = Categoria.query.filter_by(id = id).first_or_404()
    categoria = Addproduto.query.filter_by(categoria_id=get_cat.id).paginate(page=pagina,per_page=2)
    #aparecer dados na barra de nav
    categorias = Categoria.query.join(Addproduto,(Categoria.id == Addproduto.categoria_id)).all()
    marcas = Marca.query.join(Addproduto,(Marca.id == Addproduto.marca_id)).all()

    return render_template('/produtos/index.html', categoria = categoria, categorias = categorias, marcas = marcas,get_cat = get_cat, title = f"Produtos {get_cat.name} - Pág {pagina}")

@app.route('/produto/<int:id>', methods=['GET','POST'])
def pagina_unica(id):
    produto = Addproduto.query.get_or_404(id)
    marcas = Marca.query.join(Addproduto,(Marca.id == Addproduto.marca_id)).all()
    categorias = Categoria.query.join(Addproduto,(Categoria.id == Addproduto.categoria_id)).all()

    return render_template('/produtos/pagina_unica.html', produto = produto, marcas = marcas, categorias = categorias, title = produto.name)

@app.route('/pesquisa/', methods=['GET', 'POST'])
def pesquisa():
    pagina = request.args.get('pagina', 1, type=int)
    termo = request.args.get('query', '').strip()  # Obtém o valor da pesquisa , strip é o mesmo que trim() do js

    # Filtra os produtos se o usuário digitou algo na barra de pesquisa
    if termo:
    
        produtosPesquisa = Addproduto.query.filter(
            Addproduto.name.ilike(f'%{termo}%'),  # Aqui usamos `ilike` para ignorar maiúsculas/minúsculas
            Addproduto.stock > 0
        ).order_by(Addproduto.id.desc()).paginate(page=pagina, per_page=8)
        if produtosPesquisa.items == []:
            mensagem = "Nenhum item encontrado para a pesquisa."
            flash(mensagem)
    else:
        # Se não houver pesquisa, exibe todos os produtos com estoque disponível
        produtosPesquisa = Addproduto.query.filter(Addproduto.stock > 0).order_by(Addproduto.id.desc()).paginate(page=pagina, per_page=8)

    # Aparece dados na barra de navegação (marcas e categorias)
    marcas = Marca.query.join(Addproduto, (Marca.id == Addproduto.marca_id)).all()
    categorias = Categoria.query.join(Addproduto, (Categoria.id == Addproduto.categoria_id)).all()

    return render_template('/produtos/index.html', produtosPesquisa=produtosPesquisa, marcas=marcas, categorias=categorias, termo = termo, title = f"Pesquisar - Pág {pagina}")

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
    return render_template('/produtos/addmarca.html',marcas = 'marcas', title = "Registrar Fabricante")

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
    return render_template('/produtos/addmarca.html', title = "Registrar Categoria")

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

@app.route('/addproduto', methods=['GET', 'POST'])
def addproduto():
    if 'email' not in session:
        flash(f'Por Favor fazer seu login no sistema', 'danger')
        return redirect(url_for('login'))

    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    form = Addprodutos(request.form)

    print(request.method)
    print(request.form)
    print(request.files)
    print(form.errors)
    print(form.data)

    if request.method == 'POST':
        print("Formulario Validado")
        print(form.errors)
        print(request.files)
        print(request.form)

        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        marca = request.form.get('marca')
        categoria = request.form.get('categoria')

        image_1_file = request.files.get('image_1')
        image_2_file = request.files.get('image_2')
        image_3_file = request.files.get('image_3')

        def save_image(image_file):
            if image_file:
                filename = secure_filename(image_file.filename)
                random_hex = secrets.token_hex(10)
                _, f_ext = os.path.splitext(filename)
                image_fn = random_hex + f_ext
                image_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], image_fn)
                try:
                    image_file.save(image_path)
                    print(f"Imagem salva em: {image_path}")
                except Exception as e:
                    print(f"Erro ao salvar imagem: {e}")
                return image_fn
            return None

        image_1_fn = save_image(image_1_file)
        image_2_fn = save_image(image_2_file)
        image_3_fn = save_image(image_3_file)

        print(f"Image 1 Filename: {image_1_fn}")
        print(f"Image 2 Filename: {image_2_fn}")
        print(f"Image 3 Filename: {image_3_fn}")

        addpro = Addproduto(name=name, price=price, discount=discount, stock=stock, colors=colors, desc=desc, marca_id=marca, categoria_id=categoria, image_1=image_1_fn, image_2=image_2_fn, image_3=image_3_fn)
        db.session.add(addpro)
        try:
            db.session.commit()
            print("Commit realizado com sucesso")
        except Exception as e:
            print(f"Erro no commit: {e}")
        print(os.listdir(app.config['UPLOADED_PHOTOS_DEST']))
        flash(f'O produto {name} foi cadastrado com sucesso', 'success')
        return redirect(url_for('admin'))

    return render_template('/produtos/addproduto.html', title='Cadastrar Produto', form=form, marcas=marcas, categorias=categorias)

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
        produto.name = form.name.data
        produto.price = form.price.data
        produto.desc = form.discription.data
        produto.marca_id = marca
        produto.categoria_id = categoria
        produto.stock = form.stock.data
        produto.colors = form.colors.data
        produto.discount = form.discount.data

        def update_image(image, current_image):
            if image:
                filename = secure_filename(image.filename)
                random_hex = secrets.token_hex(10)
                _, f_ext = os.path.splitext(filename)
                image_fn = random_hex + f_ext
                image_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], image_fn)
                image.save(image_path)
                if current_image:
                    try:
                        os.unlink(os.path.join(current_app.root_path, 'static/images/' + current_image))
                    except:
                        pass
                return image_fn
            return current_image

        produto.image_1 = update_image(request.files.get('image_1'), produto.image_1)
        produto.image_2 = update_image(request.files.get('image_2'), produto.image_2)
        produto.image_3 = update_image(request.files.get('image_3'), produto.image_3)

        db.session.commit()
        flash(f'Produto foi atualizado com sucesso', 'success')
        return redirect('/admin')

    form.name.data = produto.name
    form.price.data = produto.price
    form.discription.data = produto.desc
    form.stock.data = produto.stock
    form.colors.data = produto.colors
    form.discount.data = produto.discount

    return render_template('/produtos/updateproduto.html', title='Atualizar Produtos', form=form, marcas=marcas, categorias=categorias, produto=produto)

# ... (outras rotas)

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