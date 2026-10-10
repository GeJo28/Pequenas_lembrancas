from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TelField, TextAreaField, RadioField, FloatField, HiddenField
from wtforms.validators import DataRequired, NumberRange

class FormCarrinhoBrigadeiro(FlaskForm):
    quantidade = IntegerField(default=0)
    botao_submit_brigadeiro = SubmitField('Adicionar')

class FormCarrinhoCoxinha(FlaskForm):
    produto_id = HiddenField()
    quantidade = IntegerField(default=0)
    botao_submit_coxinha = SubmitField('Adicionar')

class FormEntrega(FlaskForm):
    rua_logradouro = StringField(validators=[DataRequired()])
    numero = IntegerField(validators=[DataRequired()])
    complemento = StringField()
    bairro = StringField(validators=[DataRequired()])
    nome = StringField(validators=[DataRequired()])
    celular = TelField(validators=[DataRequired()])
    referencia = TextAreaField()
    botao_submit_entrega = SubmitField('Ir para o Pagamento')