from flask import Flask, render_template
import funcoesdb as db
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def videos():
    conexao = db.abrirConexao()
    videos = db.listarVideos(conexao)
    return render_template("videos.html", videos=videos)


if __name__ == "__main__":
    app.run(debug=True)
