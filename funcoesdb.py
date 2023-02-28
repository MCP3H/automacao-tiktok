# baixar o MySQL, se for Windows acesse o link: https://dev.mysql.com/downloads/installer/
import mysql.connector  # baixar o connector: pip install mysql-connector-python
import datetime

# CREATE TABLE `video` (
#   `idVideo` int NOT NULL AUTO_INCREMENT,
#   `videoURL` varchar(255) DEFAULT NULL,
#   `videoData` datetime DEFAULT NULL,
#   `apareceCachorro` tinyint DEFAULT 0,
#   `percentualCachorro` float DEFAULT NULL,
#   `apareceGato` tinyint DEFAULT 0,
#   `percentualGato` float DEFAULT NULL,
#   `avaliado` tinyint DEFAULT 0,
#   `motivo` varchar(255) DEFAULT NULL,
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


def listarVideosNaoAvaliados():
    comando = f'SELECT * FROM video WHERE avaliado = 0'
    cursor.execute(comando)
    resultado = cursor.fetchall()
    return resultado


def salvarVideo(videoURL):
    videoData = datetime.datetime.now()
    comando = f'INSERT INTO video (videoURL, videoData) VALUES ("{videoURL}", "{videoData}")'
    cursor.execute(comando)
    conexao.commit()


def salvarVideoCachorro(videoURL, percentualCachorro):
    videoData = datetime.datetime.now()
    comando = f'INSERT INTO video (videoURL, videoData, apareceCachorro, percentualCachorro) VALUES ("{videoURL}", "{videoData}", 1, {percentualCachorro})'
    cursor.execute(comando)
    conexao.commit()


def salvarVideoGato(videoURL, percentualGato):
    videoData = datetime.datetime.now()
    comando = f'INSERT INTO video (videoURL, videoData, apareceGato, percentualGato) VALUES ("{videoURL}", "{videoData}", 1, {percentualGato})'
    cursor.execute(comando)
    conexao.commit()


def salvarVideoCachorroGato(videoURL, percentualCachorro, percentualGato):
    videoData = datetime.datetime.now()
    comando = f'INSERT INTO video (videoURL, videoData, apareceCachorro, percentualCachorro, apareceGato, percentualGato) VALUES ("{videoURL}", "{videoData}", 1, {percentualCachorro}, 1, {percentualGato})'
    cursor.execute(comando)
    conexao.commit()


def salvarMotivo(idVideo, motivo):
    comando = f'UPDATE video SET avaliado = 1, motivo = "{motivo}" WHERE idVideo = {idVideo}'
    cursor.execute(comando)
    conexao.commit()


def fecharConexao():
    cursor.close()
    conexao.close()
