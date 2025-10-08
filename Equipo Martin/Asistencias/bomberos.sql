-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.32-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.11.0.7065
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para bomberos
CREATE DATABASE IF NOT EXISTS `bomberos` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `bomberos`;

-- Volcando estructura para tabla bomberos.asistencia_evento_cabecera
CREATE TABLE IF NOT EXISTS `asistencia_evento_cabecera` (
  `id_asistencia_cabecera` int(10) NOT NULL AUTO_INCREMENT,
  `id_evento` int(4) NOT NULL,
  `fecha` date NOT NULL,
  `nro_planilla` int(10) NOT NULL,
  `confirmada` varchar(1) NOT NULL,
  `fecha_insert` date NOT NULL,
  `nro_legajo_responsable` int(10) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_asistencia_cabecera`),
  KEY `id_evento` (`id_evento`),
  KEY `legajo_responsable` (`nro_legajo_responsable`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bomberos.asistencia_evento_detalle
CREATE TABLE IF NOT EXISTS `asistencia_evento_detalle` (
  `id_asistencia_evento_detalle` int(10) NOT NULL AUTO_INCREMENT,
  `nro_legajo` int(10) NOT NULL,
  `licencia` varchar(1) NOT NULL,
  `id_asistencia_cabecera` int(10) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_asistencia_evento_detalle`),
  KEY `nro_legajo` (`nro_legajo`),
  KEY `id_asistencia_cabecera` (`id_asistencia_cabecera`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bomberos.conducta_personal
CREATE TABLE IF NOT EXISTS `conducta_personal` (
  `id_conducta` int(10) NOT NULL AUTO_INCREMENT,
  `nro_legajo` int(10) NOT NULL,
  `puntos` int(1) NOT NULL,
  `mes` int(2) NOT NULL,
  `anio` int(4) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_conducta`),
  KEY `nro_legajo` (`nro_legajo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bomberos.eventos
CREATE TABLE IF NOT EXISTS `eventos` (
  `id_evento` int(4) NOT NULL,
  `evento` varchar(100) NOT NULL,
  `puntos` int(2) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_evento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bomberos.personal
CREATE TABLE IF NOT EXISTS `personal` (
  `nro_legajo` int(10) NOT NULL,
  `apellido_nombre` varchar(100) NOT NULL,
  `dni` int(8) NOT NULL,
  `user` varchar(20) NOT NULL,
  `pass` varchar(8) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`nro_legajo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bomberos.unidades
CREATE TABLE IF NOT EXISTS `unidades` (
  `id_unidad` int(5) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `operativa` int(1) NOT NULL,
  PRIMARY KEY (`id_unidad`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- La exportación de datos fue deseleccionada.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

-- Insertar datos de ejemplo en PERSONAL
INSERT INTO personal (nro_legajo, apellido_nombre, dni, user, pass) VALUES
('Administrador Admin',10000000,'jefe'   ,'jefe'),
('AnaAlvarez'         ,20000000,'user1'  ,'user1'),
('BrunoBenitez'       ,30000000,'user2'  ,'user2'),
('CarlaCortez'        ,40000000,'user3'  ,'user3'),
('DiegoDiaz'          ,41000000,'user4'  ,'user4'),
('ElenaEscobar'       ,42000000,'user5'  ,'user5'),
('FernandoFernandez'  ,42000000,'user6'  ,'user6'),
('GabrielaGomez'      ,42100000,'user7'  ,'user7'),
('HugoHerrera'        ,42200000,'user8'  ,'user8'),
('IsabelIglesias'     ,42300000,'user9'  ,'user9'),
('JavierJuarez'       ,42400000,'user10' ,'user10'),
('KarinaKruger'       ,42500000,'user11' ,'user11'),
('LuisLopez'          ,42600000,'user12' ,'user12'),
('MariaMartinez'      ,42700000,'user13' ,'user13'),
('NicolasNavarro'     ,42800000,'user14' ,'user14'),
('OlgaOrtega'         ,42900000,'user15' ,'user15');