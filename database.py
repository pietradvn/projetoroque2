import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conexao = self.create_connection()

    def create_connection(self):
        try:
            conexao = sqlite3.connect(self.db_file, check_same_thread=False)
            return conexao
        except sqlite3.Error as e:
            print("Erro ao conectar ao SQLite:", e)
            return None

    def create_tables(self):
        if not self.conexao:
            print("Falha na conexão com o banco de dados.")
            return

        try:
            cursor = self.conexao.cursor()
            cursor.execute("DROP TABLE IF EXISTS usuarios")

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                );
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    categoria TEXT,
                    preco REAL,
                    quantidade INTEGER
                );
            ''')
            self.conexao.commit()
        except sqlite3.Error as e:
            print("Erro ao criar tabelas:", e)
        finally:
            if 'cursor' in locals():
                cursor.close()

    def cadastrar_usuario(self, username, password, email):
        """Cadastra um novo usuário no banco de dados"""
        if not self.conexao:
            print("Falha na conexão com o banco de dados.")
            return

        try:
            cursor = self.conexao.cursor()
            cursor.execute("INSERT INTO usuarios (username, password, email) VALUES (?, ?, ?)",
                           (username, password, email))
            self.conexao.commit()
            print("Usuário cadastrado com sucesso.")
        except sqlite3.Error as e:
            print("Erro ao cadastrar usuário:", e)
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_usuario(self, username):
        """Obtém os dados de um usuário pelo nome de usuário"""
        if not self.conexao:
            print("Falha na conexão com o banco de dados.")
            return None

        try:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
            usuario = cursor.fetchone()
            return usuario
        except sqlite3.Error as e:
            print("Erro ao buscar usuário:", e)
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()

    def listar_usuarios(self):
        """Lista todos os usuários no banco de dados"""
        if not self.conexao:
            print("Falha na conexão com o banco de dados.")
            return []

        try:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()
            return usuarios
        except sqlite3.Error as e:
            print("Erro ao listar usuários:", e)
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()

    def cadastrar_produto(self, nome, descricao, categoria, preco, quantidade):
        """Cadastra um novo produto no banco de dados"""
        if not self.conexao:
            print("Falha na conexão com o banco de dados.")
            return

        try:
            cursor = self.conexao.cursor()
            cursor.execute("INSERT INTO produtos (nome, descricao, categoria, preco, quantidade) VALUES (?, ?, ?, ?, ?)",
                           (nome, descricao, categoria, preco, quantidade))
            self.conexao.commit()
            print("Produto cadastrado com sucesso.")
        except sqlite3.Error as e:
            print("Erro ao cadastrar produto:", e)
        finally:
            if 'cursor' in locals():
                cursor.close()

    def listar_produtos(self):
        """Lista todos os produtos no banco de dados"""
        if not self.conexao:
            print("Falha na conexão com o banco de dados.")
            return []

        try:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM produtos")
            produtos = cursor.fetchall()
            return produtos
        except sqlite3.Error as e:
            print("Erro ao listar produtos:", e)
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
