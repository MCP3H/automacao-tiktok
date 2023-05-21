from flask import Flask, render_template
import banco as db
import automacao as pya
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def videos():
    conexao = db.abrirConexao()
    list_video = db.listarVideos(conexao)
    return render_template("videos.html", videos=list_video)


if __name__ == "__main__":
    pya.abrirLocalhost()
    app.run(debug=False)

