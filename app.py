from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:dbfdp09@localhost:5433/minicrm"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurações do banco PostgreSQL
DB_HOST = 'localhost'
DB_NAME = 'minicrm'
DB_PORT = '5433'
DB_USER = 'postgres'
DB_PASSWORD = 'dbfdp09'

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

@app.route('/')
def index():
    return redirect(url_for('listar_clientes'))

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT COUNT(*) FROM cliente')
    total_clientes = cur.fetchone()[0]

    cur.execute('SELECT COUNT(*) FROM cliente')  # Atualize se houver campo de "ativo"
    clientes_ativos = cur.fetchone()[0]

    cur.close()
    conn.close()

    return render_template('dashboard.html',
                           total_clientes=total_clientes,
                           clientes_ativos=clientes_ativos)

@app.route('/clientes')
def listar_clientes():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM cliente')
    clientes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('clientes/listar.html', clientes=clientes)

@app.route('/clientes/novo', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        possui_empresa = request.form.get('possui_empresa')
        empresa = request.form.get('empresa') if possui_empresa == 'sim' else None

        if not nome or not email:
            flash('Nome e e-mail são obrigatórios.', 'danger')
            return redirect(url_for('cadastrar_cliente'))

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO cliente (nome, email, telefone, empresa) VALUES (%s, %s, %s, %s)',
            (nome, email, telefone, empresa)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash('Cliente cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_clientes'))

    return render_template('clientes/cadastrar.html')

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute('SELECT * FROM cliente WHERE id_cliente = %s', (id,))
    cliente = cur.fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        empresa = request.form['empresa']  # Certifique-se de que esse campo existe no form

        cur.execute('''
            UPDATE cliente
            SET nome = %s, email = %s, telefone = %s, empresa = %s
            WHERE id_cliente = %s
        ''', (nome, email, telefone, empresa, id))
        conn.commit()

        cur.close()
        conn.close()
        return redirect(url_for('listar_clientes'))

    cur.close()
    conn.close()
    return render_template('clientes/editar.html', cliente=cliente)

    # Busca os dados do cliente
    cur.execute('SELECT * FROM cliente WHERE id_cliente = %s', (id,))
    cliente = cur.fetchone()

    # Debug: verificando se o cliente foi encontrado
    print(f"Cliente encontrado: {cliente}")

    cur.close()
    conn.close()

    # Caso cliente não encontrado, redireciona ou exibe mensagem
    if not cliente:
        print("Cliente não encontrado!")
        return redirect(url_for('listar_clientes'))  # Ou qualquer página de erro

    return render_template('clientes/editar.html', cliente=cliente)

@app.route('/excluir/<int:id_cliente>', methods=["POST"])
def excluir_cliente(id_cliente):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM cliente WHERE id_cliente = %s', (id_cliente,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('listar_clientes'))

# CONTATOS

@app.route('/clientes/<int:id_cliente>/contatos/novo', methods=['GET', 'POST'])
def novo_contato(id_cliente):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if request.method == 'POST':
        tipo = request.form['tipo']
        descricao = request.form['descricao']
        data_contato = request.form['data_contato']

        cur.execute('''
            INSERT INTO contato (id_cliente, tipo, descricao, data_contato)
            VALUES (%s, %s, %s, %s)
        ''', (id_cliente, tipo, descricao, data_contato))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('listar_contatos', id_cliente=id_cliente))

    cur.execute('SELECT nome FROM cliente WHERE id_cliente = %s', (id_cliente,))
    cliente = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('contatos/novo.html', cliente_nome=cliente['nome'], id_cliente=id_cliente)

@app.route('/clientes/<int:id_cliente>/contatos')
def listar_contatos(id_cliente):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT nome FROM cliente WHERE id_cliente = %s', (id_cliente,))
    cliente = cur.fetchone()
    cur.execute('SELECT * FROM contato WHERE id_cliente = %s', (id_cliente,))
    contatos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('contatos/listar.html', contatos=contatos, cliente_nome=cliente['nome'], id_cliente=id_cliente)

@app.route('/contatos/editar/<int:id>', methods=['GET', 'POST'])
def editar_contato(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM contato WHERE id = %s', (id,))
    contato = cur.fetchone()

    if request.method == 'POST':
        tipo = request.form['tipo']
        descricao = request.form['descricao']

        cur.execute('UPDATE contato SET tipo = %s, descricao = %s WHERE id = %s', (tipo, descricao, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(f'/clientes/{contato["id_cliente"]}/contatos')

    cur.close()
    conn.close()
    return render_template('contatos/editar.html', contato=contato)

@app.route('/contatos/excluir/<int:id>', methods=['POST'])
def excluir_contato(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM contato WHERE id = %s', (id,))
    contato = cur.fetchone()

    if contato:
        cur.execute('DELETE FROM contato WHERE id = %s', (id,))
        conn.commit()
    cur.close()
    conn.close()
    return redirect(f'/clientes/{contato["id_cliente"]}/contatos')

# TAREFAS

@app.route('/clientes/<int:id_cliente>/tarefas/novo', methods=['GET', 'POST'])
def nova_tarefa(id_cliente):
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data_agendada = request.form['data_agendada']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO agendamento (titulo, descricao, data_agendada, concluida, id_cliente)
            VALUES (%s, %s, %s, %s, %s)
        ''', (titulo, descricao, data_agendada, False, id_cliente))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('listar_tarefas', id_cliente=id_cliente))

    return render_template('tarefas/novo.html', id_cliente=id_cliente)

@app.route('/clientes/<int:id_cliente>/tarefas')
def listar_tarefas(id_cliente):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cur.execute('SELECT nome FROM cliente WHERE id_cliente = %s', (id_cliente,))
    cliente = cur.fetchone()
    
    if cliente is None:
        cur.close()
        conn.close()
        return "Cliente não encontrado", 404

    cur.execute('SELECT * FROM agendamento WHERE id_cliente = %s', (id_cliente,))
    tarefas = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('tarefas/listar.html', tarefas=tarefas, cliente_nome=cliente['nome'], id_cliente=id_cliente)

@app.route('/clientes/<int:id_cliente>/tarefas/<int:id_agendamento>/concluir')
def concluir_tarefa(id_cliente, id_agendamento):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE agendamento SET concluida = TRUE WHERE id_agendamento = %s', (id_agendamento,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('listar_tarefas', id_cliente=id_cliente))

@app.route('/clientes/<int:id_cliente>/tarefas/<int:id_agendamento>/excluir')
def excluir_tarefa(id_cliente, id_agendamento):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM agendamento WHERE id_agendamento = %s', (id_agendamento,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('listar_tarefas', id_cliente=id_cliente))

@app.route('/clientes/<int:id_cliente>/tarefas/<int:id_agendamento>/editar', methods=['GET', 'POST'])
def editar_tarefa(id_cliente, id_agendamento):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data_agendada = request.form['data_agendada']

        cur.execute('''
            UPDATE agendamento
            SET titulo = %s, descricao = %s, data_agendada = %s
            WHERE id_agendamento = %s
        ''', (titulo, descricao, data_agendada, id_agendamento))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('listar_tarefas', id_cliente=id_cliente))

    cur.execute('SELECT * FROM agendamento WHERE id_agendamento = %s', (id_agendamento,))
    tarefa = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('tarefas/editar.html', tarefa=tarefa, id_cliente=id_cliente)

if __name__ == '__main__':
    app.run(debug=True)
