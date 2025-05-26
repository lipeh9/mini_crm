# 🧠 Mini-CRM - Sistema de Gestão de Clientes

Mini-CRM é um sistema simples de gerenciamento de clientes, tarefas e contatos, desenvolvido com **Flask**, **SQLAlchemy**, **SQLite** e HTML/CSS (Jinja2). O projeto implementa funcionalidades básicas de um CRM com separação por módulos, formulários, templates organizados e interface leve.

---

## ✨ Funcionalidades

### 🧑 Clientes

- Cadastro de novos clientes
- Listagem de todos os clientes
- Edição e atualização de dados
- Visualização de detalhes
- Exclusão

### 📞 Contatos

- Registro de contatos associados a um cliente
- Edição e exclusão de contatos
- Visualização por cliente

### ✅ Tarefas

- Cadastro de tarefas por cliente
- Marcar tarefa como concluída
- Edição e exclusão de tarefas

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **Flask**
- **SQLite** (via `SQLAlchemy`)
- **Jinja2** para templates
- **Bootstrap 5** (customizado via `static/style.css`)

---

## 📁 Estrutura de Pastas

mini_crm/
├── instance/
│ └── database.db # Banco de dados SQLite
├── static/
│ └── style.css # Estilo da aplicação
├── templates/
│ ├── base.html # Layout principal
│ ├── dashboard.html # Página inicial
│ ├── clientes/ # Templates de cliente
│ │ ├── cadastrar.html
│ │ ├── detalhes.html
│ │ ├── editar.html
│ │ ├── listar.html
│ │ └── novo.html
│ ├── contatos/ # Templates de contato
│ │ ├── editar.html
│ │ ├── listar.html
│ │ └── novo.html
│ └── tarefas/ # Templates de tarefas
│ ├── editar.html
│ ├── listar.html
│ └── nova.html
├── app.py # Roteador principal Flask
├── database.py # Configuração do banco
├── models.py # Definição das classes SQLAlchemy
├── forms.py # Formulários com WTForms
├── requirements.txt
└── README.md

---

## ▶️ Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/mini-crm.git
cd mini-crm

### 2. Crie o ambiente virtual (recomendado)

python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows

### 3. Crie os requirements.txt

pip freeze > requirements.txt

*** Seu arquivo requirements.txt pode conter:

- Flask
- Flask-WTF
- Flask-SQLAlchemy
- WTForms

### 4. Instale o Flask (se ainda não tiver):

pip install flask

*** Se estiver usando Python 3 especificamente:

python -m pip install flask

*** Verifique se a instalação foi bem-sucedida:

python -c "import flask; print(flask.__version__)"
(Deve mostrar a versão instalada, ex: 2.3.2)

### 5. Execute a aplicação

python mini_crm/app.py

Acesse no navegador: http://localhost:5000

💾 Banco de Dados
O arquivo database.db é criado automaticamente na pasta instance/ se não existir.

A estrutura do banco é gerada via SQLAlchemy (veja models.py e database.py).

📄 Licença

MIT License

Copyright (c) 2025 Felipe Silva

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
