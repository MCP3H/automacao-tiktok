# baixar o MySQL, se for Windows acesse o link: https://dev.mysql.com/downloads/installer/
import mysql.connector  # baixar o connector: pip install mysql-connector-python
from mysql.connector import Error

# USE TCC;
# DROP TABLE VIDEO;
# DROP TABLE PARAMETRO;
# CREATE TABLE `PARAMETRO` (
#   `id_parametro` int NOT NULL AUTO_INCREMENT,
#   `modelo` varchar(50) DEFAULT NULL,
#   `objeto` varchar(50) DEFAULT NULL,
#   `time_video_sec` int DEFAULT 0,
#   `perc_video` int DEFAULT 0,
#   `qt_video` int DEFAULT 0,
#   `crit_aceit` int DEFAULT 0,
#   PRIMARY KEY (`id_parametro`)
# );
# CREATE TABLE `VIDEO` (
#   `id_video` int NOT NULL AUTO_INCREMENT,
#   `id_parametro` int NOT NULL,
#   `video_link` varchar(255) DEFAULT NULL,
#   `video_data` datetime DEFAULT CURRENT_TIMESTAMP,
#   `qt_frame` int DEFAULT 0,
#   `qt_frame_param` int DEFAULT 0,
#   `valid` tinyint DEFAULT 0,
#   PRIMARY KEY (`id_video`),
#   FOREIGN KEY (`id_parametro`) REFERENCES PARAMETRO(`id_parametro`)
# );


def abrirConexao():
    conexao = None
    try:
        conexao = mysql.connector.connect(
            host='localhost', user='root', password='admin', database='tcc')
        print("Conectado.")
    except Error as err:
        print(f"Erro ao abrir conexão: '{err}'")
    return conexao


def executarQuery(conexao, query):
    cursor = conexao.cursor()
    try:
        cursor.execute(query)
        conexao.commit()
        print("Query executada.")
    except Error as err:
        print(f"Erro ao executar query: '{err}'")


def lerQuery(conexao, query):
    cursor = conexao.cursor()
    resultado = None
    try:
        cursor.execute(query)
        resultado = cursor.fetchall()
        print("Registros retornados: ", cursor.rowcount)
        return resultado
    except Error as err:
        print(f"Erro ao ler query: '{err}'")


def fecharConexao(conexao):
    cursor = conexao.cursor()
    if (conexao.is_connected()):
        try:
            cursor.close()
            conexao.close()
            print("Desconectado.")
        except Error as err:
            print(f"Erro ao fechar conexão: '{err}'")


def listarVideos(conexao):
    resultado = lerQuery(conexao, f'SELECT v.video_link, v.video_data, v.qt_frame, v.qt_frame_param, v.valid, c.id_parametro, c.modelo, c.objeto, c.time_video_sec, c.perc_video, c.qt_video, c.crit_aceit FROM VIDEO as v LEFT JOIN PARAMETRO as c ON v.id_parametro = c.id_parametro;')
    return resultado


def verificarVideo(conexao, video_link, parametro):
    resultado = lerQuery(conexao, f'SELECT * FROM VIDEO where video_link = "{video_link}" and id_parametro = "{parametro}"')
    return resultado


def criarParametro(conexao, settings):
    modelo = settings.modelo
    objeto = settings.param
    time_video_sec = settings.time_video_sec
    perc_video = settings.perc_video
    qt_video = settings.qt_video
    crit_aceit = settings.crit_aceit

    resultado = lerQuery(conexao, f'SELECT * FROM PARAMETRO where modelo = "{modelo}" and objeto = "{objeto}" and time_video_sec = "{time_video_sec}" and perc_video = "{perc_video}" and qt_video = "{qt_video}" and crit_aceit = "{crit_aceit}"')
    
    if (len(resultado) > 0):
        return resultado[0][0]
    else:
        executarQuery(conexao, f'INSERT INTO PARAMETRO (modelo, objeto, time_video_sec, perc_video, qt_video, crit_aceit) VALUES ("{modelo}","{objeto}","{time_video_sec}","{perc_video}","{qt_video}","{crit_aceit}")')
        resultado = lerQuery(conexao, f'SELECT LAST_INSERT_ID()')
        return resultado[0][0]


def salvarVideo(conexao, id_parametro, video_link, qt_frame, qt_frame_param, valid):
    executarQuery(conexao, f'INSERT INTO video (id_parametro, video_link, qt_frame, qt_frame_param, valid) VALUES ("{id_parametro}","{video_link}","{qt_frame}","{qt_frame_param}","{valid}")')