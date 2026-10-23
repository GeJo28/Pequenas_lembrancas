import os
import secrets
import warnings

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import inspect, text

app = Flask(__name__)

secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    if os.environ.get("APP_ENV") == "production":
        raise RuntimeError("SECRET_KEY must be configured in production.")
    secret_key = secrets.token_hex(32)
    warnings.warn(
        "SECRET_KEY is not configured; development sessions will reset on restart.",
        RuntimeWarning,
        stacklevel=2,
    )

app.config["SECRET_KEY"] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plembrancas.db'

csrf = CSRFProtect(app)
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