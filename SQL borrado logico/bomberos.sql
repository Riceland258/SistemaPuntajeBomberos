-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-09-2025 a las 13:37:04
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bomberos`
--

CREATE DATABASE IF NOT EXISTS `bomberos` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `bomberos`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistencia_evento_cabecera`
--

CREATE TABLE `asistencia_evento_cabecera` (
  `id_asistencia_cabecera` int(10) NOT NULL,
  `id_evento` int(4) NOT NULL,
  `fecha` date NOT NULL,
  `nro_planilla` int(10) NOT NULL,
  `confirmada` varchar(1) NOT NULL,
  `fecha_insert` date NOT NULL,
  `nro_legajo_responsable` int(10) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistencia_evento_detalle`
--

CREATE TABLE `asistencia_evento_detalle` (
  `id_asistencia_evento_detalle` int(10) NOT NULL,
  `nro_legajo` int(10) NOT NULL,
  `licencia` varchar(1) NOT NULL,
  `id_asistencia_cabecera` int(10) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `conducta_personal`
--

CREATE TABLE `conducta_personal` (
  `id_conducta` int(10) NOT NULL,
  `nro_legajo` int(10) NOT NULL,
  `puntos` int(1) NOT NULL,
  `mes` int(2) NOT NULL,
  `anio` int(4) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `eventos`
--

CREATE TABLE `eventos` (
  `id_evento` int(4) NOT NULL,
  `evento` varchar(100) NOT NULL,
  `puntos` int(2) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personal`
--

CREATE TABLE `personal` (
  `nro_legajo` int(10) NOT NULL,
  `apellido_nombre` varchar(100) NOT NULL,
  `dni` int(8) NOT NULL,
  `user` varchar(20) NOT NULL,
  `pass` varchar(8) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `asistencia_evento_cabecera`
--
ALTER TABLE `asistencia_evento_cabecera`
  ADD PRIMARY KEY (`id_asistencia_cabecera`),
  ADD KEY `id_evento` (`id_evento`),
  ADD KEY `legajo_responsable` (`nro_legajo_responsable`);

--
-- Indices de la tabla `asistencia_evento_detalle`
--
ALTER TABLE `asistencia_evento_detalle`
  ADD PRIMARY KEY (`id_asistencia_evento_detalle`),
  ADD KEY `nro_legajo` (`nro_legajo`),
  ADD KEY `id_asistencia_cabecera` (`id_asistencia_cabecera`);

--
-- Indices de la tabla `conducta_personal`
--
ALTER TABLE `conducta_personal`
  ADD PRIMARY KEY (`id_conducta`),
  ADD KEY `nro_legajo` (`nro_legajo`);

--
-- Indices de la tabla `eventos`
--
ALTER TABLE `eventos`
  ADD PRIMARY KEY (`id_evento`);

--
-- Indices de la tabla `personal`
--
ALTER TABLE `personal`
  ADD PRIMARY KEY (`nro_legajo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `asistencia_evento_cabecera`
--
ALTER TABLE `asistencia_evento_cabecera`
  MODIFY `id_asistencia_cabecera` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `asistencia_evento_detalle`
--
ALTER TABLE `asistencia_evento_detalle`
  MODIFY `id_asistencia_evento_detalle` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `conducta_personal`
--
ALTER TABLE `conducta_personal`
  MODIFY `id_conducta` int(10) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
