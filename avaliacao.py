from flask import Flask, render_template
import funcoesdb as db

app = Flask(__name__)


@app.route('/')
def avaliacao():
    videos = db.listarVideos
    return render_template("avaliacao.html", videos=videos)


if __name__ == "__main__":
    app.run(debug=True)
