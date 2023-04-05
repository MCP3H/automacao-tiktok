# baixar o MySQL, se for Windows acesse o link: https://dev.mysql.com/downloads/installer/
import mysql.connector  # baixar o connector: pip install mysql-connector-python
import datetime

# USE TCC;
# DROP TABLE CONFIG;
# CREATE TABLE `CONFIG` (
#   `id_config` int NOT NULL AUTO_INCREMENT,
#   `param` varchar(50) DEFAULT NULL,
#   `time_video_sec` int DEFAULT 0,
#   `perc_video` decimal DEFAULT 0,
#   `time_exec_min` int DEFAULT 0,
#   `qt_video` int DEFAULT 0,
#   PRIMARY KEY (`id_config`)
# );
# DROP TABLE VIDEO;
# CREATE TABLE `VIDEO` (
#   `id_video` int NOT NULL AUTO_INCREMENT,
#   `id_config` int NOT NULL,
#   `video_url` varchar(255) DEFAULT NULL,
#   `video_data` datetime DEFAULT CURRENT_TIMESTAMP,
#   `qt_frame` int DEFAULT 0,
#   `qt_frame_param` int DEFAULT 0,
#   `valid` tinyint DEFAULT 0,
#   PRIMARY KEY (`id_video`),
#   FOREIGN KEY (`id_config`) REFERENCES CONFIG(`id_config`)
# );

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


def listarVideosURL(video_url):
    comando = f'SELECT * FROM video where video_url = "{video_url}"'
    cursor.execute(comando)
    resultado = cursor.fetchall()
    return resultado


# def listarVideosNaoAvaliados():
#     comando = f'SELECT * FROM video WHERE avaliado = 0'
#     cursor.execute(comando)
#     resultado = cursor.fetchall()
#     return resultado


def createConfig(settings):
    param = settings.param
    time_video_sec = settings.time_video_sec
    perc_video = settings.perc_video
    time_exec_min = settings.time_exec_min
    qt_video = settings.qt_video

    comando = f'SELECT * FROM config where param = "{param}" and time_video_sec = "{time_video_sec}" and perc_video = "{perc_video}" and time_exec_min = "{time_exec_min}" and qt_video = "{qt_video}" '
    cursor.execute(comando)
    resultado = cursor.fetchall()
    if (len(resultado) > 0): 
        return resultado[0][0]
    else:
        comando = f'INSERT INTO config (param, time_video_sec, perc_video, time_exec_min, qt_video) VALUES ("{param}","{time_video_sec}","{perc_video}","{time_exec_min}","{qt_video}")'
        cursor.execute(comando)
        conexao.commit()
        return cursor.lastrowid


def salvarVideo(id_config, video_url, qt_frame, qt_frame_param, valid):
    comando = f'INSERT INTO video (id_config, video_url, qt_frame, qt_frame_param, valid) VALUES ("{id_config}","{video_url}","{qt_frame}","{qt_frame_param}","{valid}")'
    cursor.execute(comando)
    conexao.commit()


# def salvarMotivo(idVideo, motivo):
#     comando = f'UPDATE video SET avaliado = 1, motivo = "{motivo}" WHERE idVideo = {idVideo}'
#     cursor.execute(comando)
#     conexao.commit()


def fecharConexao():
    cursor.close()
    conexao.close()
