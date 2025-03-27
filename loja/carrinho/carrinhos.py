from flask import redirect, render_template, url_for, flash, request, session, current_app
from loja import db, app
from loja.produtos.models import Addproduto, Marca, Categoria

#adicionar item ao carrinho com alto incremento
def M_Dicionarios(dic1,dic2):
    if isinstance(dic1, list) and isinstance(dic2, list):
        return dic1 + dic2
    elif isinstance(dic1, dict) and isinstance(dic2, dict):
        return dict(list(dic1.items()) + list(dic2.items()))



@app.route('/addCart', methods=['POST'])
def addCarrinho():
    try:
        produto_id = request.form.get('produto_id')
        quantity = request.form.get('quantity')
        color = request.form.get('colors')
        produto = Addproduto.query.filter_by(id = produto_id).first()

        if produto_id and quantity and color and request.method == 'POST':
            DicItems = {produto_id:{'name':produto.name,'price':float(produto.price), 'discount': produto.discount, 'color': color, 'quantity': quantity, 'image': produto.image_1, 'colors': produto.colors, 'stock': produto.stock}}
            if 'LojainCarrinho' in session:
                print(session['LojainCarrinho'])
                if produto_id in session['LojainCarrinho']:
                    print("O produto já foi adicionado ao carrinho")
                else:
                    session['LojainCarrinho'] = M_Dicionarios(session['LojainCarrinho'], DicItems)
                    return redirect(request.referrer)
            else:
                session['LojainCarrinho'] = DicItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carros')
def getCart():
    marcas = Marca.query.join(Addproduto, (Marca.id == Addproduto.marca_id)).all()
    categorias = Categoria.query.join(Addproduto, (Categoria.id == Addproduto.categoria_id)).all()

    if 'LojainCarrinho' not in session:
        return redirect(request.referrer)

    subtotal1 = 0
    for key, produto in session['LojainCarrinho'].items():
        discount = (produto['discount'] / 100) * float(produto['price'])
        subtotal1 += (float(produto['price']) - discount) * int(produto['quantity'])

    # Imposto é calculado após o subtotal, com 6% do valor total após os descontos
    imposto = round(0.06 * subtotal1, 2)  # Imposto de 6%
    valorpagar = round(subtotal1 + imposto, 2)

    return render_template('produtos/carros.html', marcas = marcas, categorias = categorias, title="Carrinho de Compras", imposto = imposto, valorpagar = valorpagar)

@app.route('/updateCarro/<int:code>', methods = ['POST'])
def updateCarro(code):
    if 'LojainCarrinho' not in session and len(session['LojainCarrinho']) < 0:
        return redirect(url_for('home'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['LojainCarrinho'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Carrinho foi Atualizado')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))


@app.route('/vazio')
def vazio_Cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)