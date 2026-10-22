from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b38883662ebdc3ee251f7eb9d1566ec0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plembrancas.db'

database = SQLAlchemy(app)

from pequenasLembrancas import routes

with app.app_context():
    inspector = inspect(database.engine)
    if inspector.has_table("entrega"):
        colunas_entrega = {
            coluna["name"]
            for coluna in inspector.get_columns("entrega")
        }
        with database.engine.begin() as conexao:
            if "criado_em" not in colunas_entrega:
                conexao.execute(
                    text("ALTER TABLE entrega ADD COLUMN criado_em DATETIME")
                )
            conexao.execute(
                text(
                    "UPDATE entrega SET criado_em = CURRENT_TIMESTAMP "
                    "WHERE criado_em IS NULL"
                )
            )