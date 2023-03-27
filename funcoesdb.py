# baixar o MySQL, se for Windows acesse o link: https://dev.mysql.com/downloads/installer/
import mysql.connector  # baixar o connector: pip install mysql-connector-python
import datetime

# CREATE TABLE `video` (
#   `idVideo` int NOT NULL AUTO_INCREMENT,
#   `videoURL` varchar(255) DEFAULT NULL,
#   `videoData` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`idVideo`)
# )

# create, update, delete, usar: conexao.commit()
# read, usar: cursor.fetchall()

conexao = mysql.connector.connect(
    host='localhost', user='root', password='admin', database='tcc')

cursor = conexao.cursor()


def listarVideos():
    comando = f'SELECT * FROM video'
    cursor.execute(comando)
    resultado = cursor.fetchall()
    return resultado


def listarVideosURL(videoURL):
    comando = f'SELECT * FROM video where videoURL = "{videoURL}"'
    cursor.execute(comando)
    resultado = cursor.fetchall()
    return resultado


# def listarVideosNaoAvaliados():
#     comando = f'SELECT * FROM video WHERE avaliado = 0'
#     cursor.execute(comando)
#     resultado = cursor.fetchall()
#     return resultado


def salvarVideo(videoURL):
    comando = f'INSERT INTO video (videoURL) VALUES ("{videoURL}")'
    cursor.execute(comando)
    conexao.commit()


# def salvarMotivo(idVideo, motivo):
#     comando = f'UPDATE video SET avaliado = 1, motivo = "{motivo}" WHERE idVideo = {idVideo}'
#     cursor.execute(comando)
#     conexao.commit()


def fecharConexao():
    cursor.close()
    conexao.close()
