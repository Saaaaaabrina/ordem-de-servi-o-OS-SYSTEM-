from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("os.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS ordens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    status TEXT NOT NULL,
                    valor REAL NOT NULL
                )''')

@app.route('/')
def index():
    with sqlite3.connect("os.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ordens ORDER BY id DESC") 
        ordens = cursor.fetchall()
    return render_template('index.html', ordens=ordens)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    cliente = request.form['cliente']
    numero = request.form['numero']  # Esse campo não está sendo usado, se não for necessário pode ser removido.
    valor = request.form['valor']  # Captura o valor do campo do formulário
    descricao = request.form['descricao']
    status = "Aberto"
    
    with sqlite3.connect("os.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ordens (cliente, descricao, status, valor) VALUES (?, ?, ?, ?)",
                       (cliente, descricao, status, valor))  # Inserir também o valor
        conn.commit()
    
    return redirect(url_for('index'))


@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    novo_status = request.form['status']
    with sqlite3.connect("os.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE ordens SET status = ? WHERE id = ?", (novo_status, id))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/excluir/<int:id>')
def excluir(id):
    with sqlite3.connect("os.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ordens WHERE id = ?", (id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)