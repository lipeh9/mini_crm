import sqlite3

def criar_tabelas():
    conexao = sqlite3.connect('mini_crm/database.db')
    cursor = conexao.cursor()

    # Ativa as chaves estrangeiras no SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Tabela Cliente
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cliente (
        id_cliente SERIAL PRIMARY KEY,
        empresa TEXT,
        email TEXT NOT NULL,
        nome TEXT NOT NULL,
        telefone TEXT,
        data_cadastro TIMESTAMP DEFAULT now() NOT NULL
    );
''')

    # Tabela Contato
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contato (
        id_contato SERIAL PRIMARY KEY,
        tipo_contato VARCHAR(50) NOT NULL,
        observacoes TEXT,
        data_contato DATE NOT NULL,
        fk_cliente_id_cliente INTEGER NOT NULL,
        CONSTRAINT fk_cliente
            FOREIGN KEY (fk_cliente_id_cliente)
            REFERENCES cliente(id_cliente)
            ON DELETE CASCADE
    );
''')


    # Tabela Agendamento
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS agendamento (
        id_agendamento SERIAL PRIMARY KEY,
        horario TIME NOT NULL,
        status VARCHAR(50) DEFAULT 'pendente',
        data_agendada DATE NOT NULL,
        assunto TEXT,
        fk_contato_id_contato INTEGER NOT NULL,
        CONSTRAINT fk_contato
            FOREIGN KEY (fk_contato_id_contato)
            REFERENCES contato (id_contato)
            ON DELETE CASCADE
    );
''')

    conexao.commit()
    conexao.close()
    print("Tabelas criadas com sucesso.")

if __name__ == '__main__':
    criar_tabelas()
