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
        colors = request.form.get('colors')
        produto = Addproduto.query.filter_by(id = produto_id).first()

        if produto_id and quantity and colors and request.method == 'POST':
            DicItems = {produto_id:{'name':produto.name,'price':float(produto.price), 'discount': produto.discount, 'colors': produto.colors, 'quantity': quantity, 'image': produto.image_1}}
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
    marcas = Marca.query.join(Addproduto,(Marca.id == Addproduto.marca_id)).all()
    categorias = Categoria.query.join(Addproduto,(Categoria.id == Addproduto.categoria_id)).all()
    if 'LojainCarrinho' not in session:
        return redirect(request.referrer)
    return render_template('produtos/carros.html', marcas = marcas, categorias = categorias, title="Carrinho de Compras")