from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b38883662ebdc3ee251f7eb9d1566ec0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plembrancas.db'

database = SQLAlchemy(app)

from pequenasLembrancas import routes