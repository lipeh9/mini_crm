from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()  # Instância única compartilhada

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    contatos = db.relationship('Contato', back_populates='cliente', cascade='all, delete-orphan')
    tarefas = db.relationship('Tarefa', back_populates='cliente', cascade='all, delete-orphan')

class Contato(db.Model):
    __tablename__ = 'contatos'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)  # Ex: 'email', 'telefone'
    valor = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    
    # Relacionamento
    cliente = db.relationship('Cliente', back_populates='contatos')

class Tarefa(db.Model):
    __tablename__ = 'tarefas'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    concluida = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    
    # Relacionamento
    cliente = db.relationship('Cliente', back_populates='tarefas')