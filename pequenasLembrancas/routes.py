from flask import render_template, url_for, redirect, request, session
from pequenasLembrancas import app, database
from pequenasLembrancas.forms import FormEntrega, FormCarrinhoBrigadeiro, FormCarrinhoCoxinha
from pequenasLembrancas.models import Produto, Sabor, Carrinho, ItemCarrinho, ItemCarrinhoSabor, Entrega
import uuid
from urllib.parse import quote

def obter_usuario_id():
    if "usuario_id" not in session:
        session['usuario_id'] = str(uuid.uuid4())

    return session['usuario_id']

@app.route("/", methods=['GET', 'POST'])
def index():
    usuario_id = obter_usuario_id()

    carrinho = Carrinho.query.filter_by(usuario_id=usuario_id).first()

    quantidade_carrinho = 0

    if carrinho:
        quantidade_carrinho = len(carrinho.itens)

    produto_brigadeiro = Produto.query.filter_by(
        tipo="brigadeiro"
    ).first()

    produto_coxinha = Produto.query.filter_by(
        tipo="coxinha"
    ).first()

    sabores = Sabor.query.all()

    form_carrinho_brigadeiro = FormCarrinhoBrigadeiro()
    form_carrinho_coxinha = FormCarrinhoCoxinha()

    if form_carrinho_brigadeiro.validate_on_submit() and 'botao_submit_brigadeiro' in request.form:
        sabores_ids = request.form.getlist("sabores")
        quantidade = form_carrinho_brigadeiro.quantidade.data
        carrinho = Carrinho.query.filter_by(usuario_id=usuario_id).first()

        if carrinho is None:
            carrinho = Carrinho(usuario_id=usuario_id)
            database.session.add(carrinho)
            database.session.commit()

        item_carrinho = ItemCarrinho(carrinho_id=carrinho.id, produto_id=produto_brigadeiro.id, quantidade=quantidade)
        database.session.add(item_carrinho)
        database.session.commit()

        for sabor_id in sabores_ids:
            quantidade_sabor = request.form.get(f"quantidade_{sabor_id}")
            item_sabor = ItemCarrinhoSabor(item_carrinho_id=item_carrinho.id, sabor_id=int(sabor_id), quantidade=int(quantidade_sabor))
            database.session.add(item_sabor)

        database.session.commit()

        return redirect(url_for("index"))

    if form_carrinho_coxinha.validate_on_submit() and 'botao_submit_coxinha' in request.form:
        quantidade = form_carrinho_coxinha.quantidade.data

        carrinho = Carrinho.query.filter_by(usuario_id=usuario_id).first()

        if carrinho is None:
            carrinho = Carrinho(usuario_id=usuario_id)
            database.session.add(carrinho)
            database.session.commit()

        item_carrinho = ItemCarrinho(carrinho_id=carrinho.id, produto_id=produto_coxinha.id, quantidade=quantidade)
        database.session.add(item_carrinho)
        database.session.commit()

        return redirect(url_for("index"))

    return render_template('index.html', produto_brigadeiro=produto_brigadeiro, 
                           produto_coxinha=produto_coxinha, 
                           sabores=sabores, 
                           form_carrinho_brigadeiro=form_carrinho_brigadeiro, 
                           form_carrinho_coxinha=form_carrinho_coxinha,
                           quantidade_carrinho=quantidade_carrinho
                           )

@app.route("/carrinho/remover/<int:item_id>", methods=['GET', 'POST'])
def remover_item_carrinho(item_id):
    usuario_id = obter_usuario_id()

    carrinho = Carrinho.query.filter_by(usuario_id=usuario_id).first()

    if carrinho:
        item = ItemCarrinho.query.filter_by(id=item_id, carrinho_id=carrinho.id).first()

        if item:
            database.session.delete(item)
            database.session.commit()

    return redirect(url_for("carrinho"))

@app.route("/carrinho", methods=['GET', 'POST'])
def carrinho():
    usuario_id = obter_usuario_id()

    carrinho = Carrinho.query.filter_by(usuario_id=usuario_id).first()
    total = 0
    quantidade_carrinho = 0

    if not carrinho:
        return render_template('carrinho.html', carrinho=None, itens=[], total=0, quantidade_carrinho=0)
    else:
        for item in carrinho.itens:
            total += item.produto.preco * item.quantidade
        quantidade_carrinho = len(carrinho.itens)

    return render_template('carrinho.html', carrinho=carrinho, total=total, quantidade_carrinho=quantidade_carrinho)

@app.route("/entrega", methods=['GET', 'POST'])
def entrega():
    usuario_id = obter_usuario_id()
    
    carrinho = Carrinho.query.filter_by(usuario_id=usuario_id).first()

    quantidade_carrinho = 0

    if carrinho:
        quantidade_carrinho = len(carrinho.itens)

    form_entrega = FormEntrega()

    if form_entrega.validate_on_submit() and 'botao_submit_entrega' in request.form:
        nova_entrega = Entrega(rua_logradouro=form_entrega.rua_logradouro.data,
                               numero=form_entrega.numero.data,
                               complemento=form_entrega.complemento.data,
                               bairro=form_entrega.bairro.data,
                               nome=form_entrega.nome.data,
                               celular=form_entrega.celular.data,
                               referencia=form_entrega.referencia.data
                               )

        database.session.add(nova_entrega)
        database.session.flush()

        carrinho.entrega_id = nova_entrega.id
        database.session.commit()

        return redirect(url_for('pagamento'))

    return render_template('entrega.html', form_entrega=form_entrega, quantidade_carrinho=quantidade_carrinho)

def montar_mensagem_pedido(carrinho, forma_pagamento, troco, total):
    mensagem = ""

    mensagem += "🍫 NOVO PEDIDO\n"
    mensagem += "Pequenas Lembranças\n\n"

    mensagem += "📦 PEDIDO\n\n"

    for item in carrinho.itens:

        produto = item.produto

        subtotal = (
            produto.preco *
            item.quantidade
        )

        mensagem += (
            f"{produto.nome}\n"
            f"Quantidade: {item.quantidade}\n"
        )

        if item.sabores:

            mensagem += "Sabores:\n"

            for item_sabor in item.sabores:

                mensagem += (
                    f"- {item_sabor.sabor.nome}: "
                    f"{item_sabor.quantidade}\n"
                )

        mensagem += (
            f"Subtotal: R$ {subtotal:.2f}\n\n"
        )

    mensagem += f"💰 TOTAL: R$ {total:.2f}\n\n"

    # ENTREGA

    entrega = carrinho.entrega

    mensagem += "📍 ENTREGA\n\n"

    mensagem += (
        f"Rua: {entrega.rua_logradouro}\n"
        f"Número: {entrega.numero}\n"
    )

    if entrega.complemento:
        mensagem += (
            f"Complemento: "
            f"{entrega.complemento}\n"
        )

    mensagem += (
        f"Bairro: {entrega.bairro}\n"
        f"Nome: {entrega.nome}\n"
        f"Telefone: {entrega.celular}\n"
    )

    if entrega.referencia:

        mensagem += (
            f"Referência: "
            f"{entrega.referencia}\n"
        )

    mensagem += "\n💳 PAGAMENTO\n\n"

    formas = {
        "pix": "PIX",
        "credito": "Cartão de Crédito",
        "debito": "Cartão de Débito",
        "dinheiro": "Dinheiro"
    }

    mensagem += (
        f"Forma: "
        f"{formas.get(forma_pagamento)}\n"
    )

    if forma_pagamento == "dinheiro" and troco:

        mensagem += (
            f"Troco para: "
            f"R$ {float(troco):.2f}\n"
        )

    return mensagem

@app.route("/pagamento", methods=['GET', 'POST'])
def pagamento():
    usuario_id = obter_usuario_id()
    
    carrinho = Carrinho.query.filter_by(usuario_id=usuario_id).first()
    total = 0
    quantidade_carrinho = 0

    if not carrinho:
        return redirect(url_for('index'))

    if not carrinho.itens:
        return redirect(url_for('index'))
    else:
        for item in carrinho.itens:
            total += item.produto.preco * item.quantidade
        quantidade_carrinho = len(carrinho.itens)

    if not carrinho.entrega:
        return redirect(url_for('index'))

    if request.method == 'POST':
        forma_pagamento = request.form.get('pagamento')
        troco = request.form.get('troco')

        mensagem = montar_mensagem_pedido(carrinho, forma_pagamento, troco, total)

        numero = '5511942436768' 

        link_whatsapp = f"https://wa.me/{numero}?text={quote(mensagem)}" 

        # 1. Guarda a entrega antes de apagar o carrinho
        entrega = carrinho.entrega

        # 2. Apaga o carrinho
        # Os ItemCarrinho e ItemCarrinhoSabor serão apagados
        # por causa do cascade
        database.session.delete(carrinho)

        # 3. Apaga a entrega
        if entrega:
            database.session.delete(entrega)

        # 4. Confirma as alterações no banco
        database.session.commit()

        # Apaga o identificador do usuário da sessão
        session.pop('usuario_id', None)

        return redirect(link_whatsapp)     

    return render_template('pagamento.html', quantidade_carrinho=quantidade_carrinho, total=total, carrinho=carrinho)