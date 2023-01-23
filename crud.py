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


conexao = mysql.connector.connect(
    host='localhost', user='root', password='admin', database='tcc')

cursor = conexao.cursor()

# crud

# create
videoURL = "https://www.tiktok.com/@marinarcardoso/video/7181127707084819717"
videoData = datetime.datetime.now()
comando = f'INSERT INTO video (videoURL, videoData) VALUES ("{videoURL}", "{videoData}")'
cursor.execute(comando)
conexao.commit()

# read
# comando = f'SELECT * FROM video'
# cursor.execute(comando)
# resultado = cursor.fetchall()
# print(resultado)

# update
# idVideo = 1
# videoURL = "https://www.tiktok.com/@liltarzyy/video/7174140397503925510?is_from_webapp=1&sender_device=pc&web_id=7087729147531052549"
# comando = f'UPDATE video SET videoURL = "{videoURL}" WHERE idVideo = {idVideo}'
# cursor.execute(comando)
# conexao.commit()

# delete
# idVideo = 1
# comando = f'DELETE FROM video WHERE idVideo = {idVideo}'
# cursor.execute(comando)
# conexao.commit()

# comandos: create, update, delete, usar: conexao.commit() - no caso desse sistema não, pois vamos mexer apenas com uma tabela
# comando: read, usar: cursor.fetchall()

cursor.close()
conexao.close()
