-- Cria a base de dados
CREATE DATABASE IF NOT EXISTS TCC;

-- Seleciona o banco de dados TCC
USE TCC;

-- Cria a tabela PARAMETRO
CREATE TABLE IF NOT EXISTS `PARAMETRO` (
  `id_parametro` int NOT NULL AUTO_INCREMENT,
  `modelo` varchar(50) DEFAULT NULL,
  `objeto` varchar(50) DEFAULT NULL,
  `time_video_sec` int DEFAULT 0,
  `perc_video` int DEFAULT 0,
  `qt_video` int DEFAULT 0,
  `crit_aceit` int DEFAULT 0,
  PRIMARY KEY (`id_parametro`)
);

-- Cria a tabela VIDEO
CREATE TABLE IF NOT EXISTS `VIDEO` (
  `id_video` int NOT NULL AUTO_INCREMENT,
  `id_parametro` int NOT NULL,
  `video_link` varchar(255) DEFAULT NULL,
  `video_data` datetime DEFAULT CURRENT_TIMESTAMP,
  `qt_frame` int DEFAULT 0,
  `qt_frame_param` int DEFAULT 0,
  `valid` tinyint DEFAULT 0,
  PRIMARY KEY (`id_video`),
  FOREIGN KEY (`id_parametro`) REFERENCES PARAMETRO(`id_parametro`)
);
