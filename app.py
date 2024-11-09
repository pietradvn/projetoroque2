from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key"


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///estoque.sqlite3"
db = SQLAlchemy(app)

# Modelos de banco de dados
class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Produto(db.Model):
    __tablename__ = "produtos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(100))
    categoria = db.Column(db.String(50))
    preco = db.Column(db.Float)
    quantidade = db.Column(db.Integer)


@app.route('/')
def index():
    print("Sessão atual:", session)
    if "user_id" not in session:
        print("Usuário não autenticado, redirecionando para login...")
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = Usuario.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect(url_for("index"))
        else:
            flash("Nome de usuário ou senha incorretos", "error")
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        email = request.form["email"]
        if not username or not password or not email:
            flash("Preencha todos os campos", "error")
        elif Usuario.query.filter_by(username=username).first():
            flash("Nome de usuário já existe", "error")
        elif Usuario.query.filter_by(email=email).first():
            flash("Email já registrado", "error")
        else:
            novo_usuario = Usuario(username=username, password=password, email=email)
            db.session.add(novo_usuario)
            db.session.commit()
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for("login"))
    return render_template("cadastro.html")

# Rota para listar produtos
@app.route('/produtos')
def lista_produtos():
    if "user_id" not in session:
        return redirect(url_for("login"))
    produtos = Produto.query.all()
    return render_template("produtos.html", produtos=produtos)

# Rota para criar novo produto
@app.route('/cria_produto', methods=["GET", "POST"])
def cria_produto():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        categoria = request.form["categoria"]
        preco = float(request.form["preco"])
        quantidade = int(request.form["quantidade"])
        novo_produto = Produto(nome=nome, descricao=descricao, categoria=categoria, preco=preco, quantidade=quantidade)
        db.session.add(novo_produto)
        db.session.commit()
        flash("Produto cadastrado com sucesso!", "success")
        return redirect(url_for("lista_produtos"))
    return render_template("novo_produto.html")

# Rota para editar produto
@app.route('/<int:id>/atualiza_produto', methods=["GET", "POST"])
def atualiza_produto(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    produto = Produto.query.get(id)
    if request.method == "POST":
        produto.nome = request.form["nome"]
        produto.descricao = request.form["descricao"]
        produto.categoria = request.form["categoria"]
        produto.preco = float(request.form["preco"])
        produto.quantidade = int(request.form["quantidade"])
        db.session.commit()
        flash("Produto atualizado com sucesso!", "success")
        return redirect(url_for("lista_produtos"))
    return render_template("atualiza_produto.html", produto=produto)


@app.route('/<int:id>/remove_produto')
def remove_produto(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    flash("Produto removido com sucesso!", "success")
    return redirect(url_for("lista_produtos"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
