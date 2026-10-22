from pequenasLembrancas import database
from datetime import datetime, timezone

def agora_utc():
    return datetime.now(timezone.utc).replace(tzinfo=None)

class Produto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    descricao = database.Column(database.Text, nullable=False)
    preco = database.Column(database.Float, nullable=False)
    tipo = database.Column(database.String, nullable=False)

class Sabor(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    imagem = database.Column(database.String, nullable=False)

class Carrinho(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    usuario_id = database.Column(database.String, nullable=False)
    entrega_id = database.Column(database.Integer, database.ForeignKey("entrega.id"))
    itens = database.relationship("ItemCarrinho", backref="carrinho", cascade="all, delete-orphan")
    entrega = database.relationship("Entrega")

class ItemCarrinho(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    carrinho_id = database.Column(database.Integer, database.ForeignKey("carrinho.id"), nullable=False)
    produto_id = database.Column(database.Integer, database.ForeignKey("produto.id"), nullable=False)
    quantidade = database.Column(database.Integer, nullable=False, default=0)
    produto = database.relationship("Produto")
    sabores = database.relationship("ItemCarrinhoSabor", backref="item", cascade="all, delete-orphan")

class ItemCarrinhoSabor(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    item_carrinho_id = database.Column(database.Integer, database.ForeignKey("item_carrinho.id"), nullable=False)
    sabor_id = database.Column(database.Integer, database.ForeignKey("sabor.id"))
    quantidade = database.Column(database.Integer,nullable=False)
    sabor = database.relationship("Sabor")

class Entrega(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    criado_em = database.Column(database.DateTime, nullable=False, default=agora_utc)
    rua_logradouro = database.Column(database.String, nullable=False)
    numero = database.Column(database.Integer, nullable=False)
    complemento = database.Column(database.String)
    bairro = database.Column(database.String, nullable=False)
    nome = database.Column(database.String, nullable=False)
    celular = database.Column(database.String, nullable=False)
    referencia = database.Column(database.Text)