# baixar o MySQL, se for Windows acesse o link: https://dev.mysql.com/downloads/installer/
import mysql.connector  # baixar o connector: pip install mysql-connector-python
import datetime

# CREATE TABLE `video` (
#   `idVideo` int NOT NULL AUTO_INCREMENT,
#   `videoURL` varchar(255) DEFAULT NULL,
#   `videoData` datetime DEFAULT CURRENT_TIMESTAMP,
#   `qteFrameVideo` int DEFAULT 0,
#   `apareceCachorro` tinyint DEFAULT 0,
#   `percentualCachorro` float DEFAULT 0,
#   `qteFrameCachorro` int DEFAULT 0,
#   `apareceGato` tinyint DEFAULT 0,
#   `percentualGato` float DEFAULT 0,
#   `qteFrameGato` int DEFAULT 0,
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


def salvarVideo(videoURL, qteFrameVideo, apareceCachorro, qteFrameCachorro, percentualCachorro, apareceGato, qteFrameGato, percentualGato):
    comando = f'INSERT INTO video (videoURL, qteFrameVideo, apareceCachorro, qteFrameCachorro, percentualCachorro, apareceGato, qteFrameGato, percentualGato) VALUES ("{videoURL}","{qteFrameVideo}","{apareceCachorro}","{qteFrameCachorro}","{percentualCachorro}","{apareceGato}","{qteFrameGato}","{percentualGato}")'
    cursor.execute(comando)
    conexao.commit()


def salvarMotivo(idVideo, motivo):
    comando = f'UPDATE video SET avaliado = 1, motivo = "{motivo}" WHERE idVideo = {idVideo}'
    cursor.execute(comando)
    conexao.commit()


def fecharConexao():
    cursor.close()
    conexao.close()
