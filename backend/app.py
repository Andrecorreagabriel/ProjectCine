from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import openai

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "cinema.db")

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///" + db_path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Filme(db.Model):
    __tablename__ = "filmes"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.String(1000))
    duracao = db.Column(db.Integer)
    genero = db.Column(db.String(100))
    classificacao = db.Column(db.String(10))

    def to_dict(self):
        return {"id": self.id, "titulo": self.titulo, "descricao": self.descricao,
                "duracao": self.duracao, "genero": self.genero, "classificacao": self.classificacao}

class Sala(db.Model):
    __tablename__ = "salas"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "capacidade": self.capacidade}

class Ingresso(db.Model):
    __tablename__ = "ingressos"
    id = db.Column(db.Integer, primary_key=True)
    filme_id = db.Column(db.Integer, db.ForeignKey('filmes.id'), nullable=False)
    sala_id = db.Column(db.Integer, db.ForeignKey('salas.id'), nullable=False)
    horario = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "filme_id": self.filme_id, "sala_id": self.sala_id, "horario": self.horario, "preco": self.preco}

# Initialize DB and sample data
@app.before_first_request
def init_db():
    db.create_all()
    # only insert sample if empty
    if Filme.query.count() == 0:
        f1 = Filme(titulo="Duna 2", descricao="Sci-fi épico", duracao=155, genero="Ficção", classificacao="12")
        f2 = Filme(titulo="Comédia X", descricao="Comédia para a família", duracao=95, genero="Comédia", classificacao="10")
        db.session.add_all([f1, f2])
        db.session.commit()
    if Sala.query.count() == 0:
        s1 = Sala(nome="Sala 1", capacidade=120)
        s2 = Sala(nome="Sala 2", capacidade=80)
        db.session.add_all([s1, s2])
        db.session.commit()
    if Ingresso.query.count() == 0:
        # link filme 1 sala1, filme2 sala2
        i1 = Ingresso(filme_id=1, sala_id=1, horario="2025-11-01 19:00", preco=25.0)
        i2 = Ingresso(filme_id=2, sala_id=2, horario="2025-11-01 21:00", preco=18.5)
        db.session.add_all([i1, i2])
        db.session.commit()

# Routes - API
@app.route("/api/filmes", methods=["GET"])
def listar_filmes():
    filmes = Filme.query.all()
    return jsonify([f.to_dict() for f in filmes])

@app.route("/api/filmes", methods=["POST"])
def criar_filme():
    data = request.json or {}
    f = Filme(titulo=data.get("titulo","Sem título"), descricao=data.get("descricao"), duracao=data.get("duracao"), genero=data.get("genero"), classificacao=data.get("classificacao"))
    db.session.add(f)
    db.session.commit()
    return jsonify(f.to_dict()), 201

@app.route("/api/salas", methods=["GET"])
def listar_salas():
    salas = Sala.query.all()
    return jsonify([s.to_dict() for s in salas])

@app.route("/api/salas", methods=["POST"])
def criar_sala():
    data = request.json or {}
    s = Sala(nome=data.get("nome","Sala"), capacidade=int(data.get("capacidade",0)))
    db.session.add(s); db.session.commit()
    return jsonify(s.to_dict()), 201

@app.route("/api/ingressos", methods=["GET"])
def listar_ingressos():
    ingressos = Ingresso.query.all()
    return jsonify([i.to_dict() for i in ingressos])

@app.route("/api/ingressos", methods=["POST"])
def criar_ingresso():
    data = request.json or {}
    ing = Ingresso(filme_id=int(data.get("filme_id")), sala_id=int(data.get("sala_id")), horario=data.get("horario"), preco=float(data.get("preco")))
    db.session.add(ing); db.session.commit()
    return jsonify(ing.to_dict()), 201

# Simple AI chat endpoint using OpenAI (requires OPENAI_API_KEY in env)
@app.route("/api/ia", methods=["POST"])
def chat_ia():
    payload = request.json or {}
    pergunta = payload.get("mensagem","")
    key = os.getenv("OPENAI_API_KEY", None)
    if not key:
        return jsonify({"error": "OpenAI API key not set. Place it in .env as OPENAI_API_KEY"}), 500
    openai.api_key = key
    try:
        resp = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"system","content":"Você é um assistente para um sistema de cinema."},{"role":"user","content": pergunta}], max_tokens=400)
        texto = resp["choices"][0]["message"]["content"]
        return jsonify({"resposta": texto})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve React build
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
