from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "chave"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.sqlite3'

db = SQLAlchemy(app)

class Cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    ch = db.Column(db.Integer)

    def __init__(self, nome, descricao, ch):
        self.nome = nome
        self.descricao = descricao
        self.ch = ch


@app.route('/')
def lista_cursos():
    titulo = "Lista de Cursos"
    page = request.args.get('page', 1, type=int)
    per_page = 5
    todos_cursos = Cursos.query.paginate(page=page, per_page=per_page)
    return  render_template("cursos.html", titulo = titulo, cursos=todos_cursos)

@app.route('/cria_curso', methods=["GET", "POST"])
def cria_curso():
    titulo = "Adicionar novo curso"

    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        ch = request.form.get('ch')
        if not nome or not descricao or not ch:
            flash("Preencha todos os campos do formulário", "error")
        else:
            try:
               curso = Cursos(nome, descricao, ch)
               db.session.add(curso)
               db.session.commit()
               return redirect(url_for('lista_cursos'))

            except:
                db.session.rollback()
                raise

    return render_template("novo_curso.html", titulo=titulo)

@app.route('/<int:id>/atualiza_curso', methods=["GET", "POST"])
def atualiza_curso(id):
    titulo = "Atualiza curso"

    curso = Cursos.query.filter_by(id=id).first()
    if request.method == "POST":
        nome = request.form['nome']
        descricao = request.form['descricao']
        ch = request.form['ch']
        Cursos.query.filter_by(id=id).update({"nome":nome, "descricao":descricao, "ch":ch})

        try:
            db.session.commit()
            return redirect(url_for('lista_cursos'))

        except:
            db.session.rollback()
            flash("Erro na atualização", "error")
            raise

    return render_template("atualiza_curso.html", titulo=titulo, curso=curso)


@app.route('/<int:id>/remove_curso')
def remove_curso(id):
    curso = Cursos.query.filter_by(id=id).first()
    try:
        db.session.delete(curso)
        db.session.commit()
        return redirect(url_for('lista_cursos'))
    except:
        db.session.rollback()
        flash('Erro na atualização', 'error')
        raise

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)