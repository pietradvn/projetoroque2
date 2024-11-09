import mysql.connector
from mysql.connector import Error

def criar_banco():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root753'
        )

        if conexao.is_connected():
            cursor = conexao.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS estoque;")
            print("Banco de dados 'estoque' criado com sucesso (ou já existe).")

            cursor.execute("USE estoque;")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password VARCHAR(100) NOT NULL
                
                );
            """)
            print("Tabela 'usuarios' criada com sucesso (ou já existe).")

    except Error as e:
        print("Erro ao conectar ou criar banco de dados:", e)
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão ao MySQL encerrada.")

if __name__ == "__main__":
    criar_banco()
