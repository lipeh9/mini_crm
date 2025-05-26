from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms import StringField, validators

class ClienteForm(FlaskForm):
    nome = StringField('Nome Completo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone')
    submit = SubmitField('Salvar')

class ClienteForm(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    telefone = StringField('Telefone')


class ContatoForm(FlaskForm):
    tipo = SelectField('Tipo', choices=[('email', 'Email'), ('telefone', 'Telefone')], validators=[DataRequired()])
    valor = StringField('Valor', validators=[DataRequired()])
    submit = SubmitField('Adicionar')

class TarefaForm(FlaskForm):
    descricao = StringField('Descrição', validators=[DataRequired()])
    submit = SubmitField('Adicionar')