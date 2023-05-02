from flask import Flask, render_template
import banco as db
import automacao as pya
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def videos():
    conexao = db.abrirConexao()
    videos = db.listarVideos(conexao)
    return render_template("videos.html", videos=videos)


if __name__ == "__main__":
    pya.abrirLocalhost()
    app.run(debug=False)
    
