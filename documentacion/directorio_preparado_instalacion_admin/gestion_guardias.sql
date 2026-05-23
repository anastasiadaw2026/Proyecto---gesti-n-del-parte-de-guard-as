-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: mysql_daw1
-- Generation Time: May 23, 2026 at 04:16 PM
-- Server version: 9.7.0
-- PHP Version: 8.3.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gestion_guardias`
--

-- --------------------------------------------------------

--
-- Table structure for table `aulas`
--

CREATE TABLE `aulas` (
  `nombre` varchar(100) COLLATE utf8mb3_spanish2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish2_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cursos`
--

CREATE TABLE `cursos` (
  `nombre` varchar(100) COLLATE utf8mb3_spanish2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish2_ci;

-- --------------------------------------------------------

--
-- Table structure for table `guardias`
--

CREATE TABLE `guardias` (
  `id` varchar(100) COLLATE utf8mb3_spanish2_ci NOT NULL,
  `dia` date NOT NULL,
  `hora` varchar(100) COLLATE utf8mb3_spanish2_ci NOT NULL DEFAULT '',
  `curso` varchar(100) COLLATE utf8mb3_spanish2_ci NOT NULL DEFAULT '',
  `aula` varchar(100) COLLATE utf8mb3_spanish2_ci NOT NULL DEFAULT '',
  `tarea` varchar(1) COLLATE utf8mb3_spanish2_ci NOT NULL DEFAULT 'N',
  `ficheros` mediumtext COLLATE utf8mb3_spanish2_ci
) ;

-- --------------------------------------------------------

--
-- Table structure for table `horas`
--

CREATE TABLE `horas` (
  `nombre` varchar(100) COLLATE utf8mb3_spanish2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish2_ci;

-- --------------------------------------------------------

--
-- Table structure for table `profesores`
--

CREATE TABLE `profesores` (
  `id` varchar(100) COLLATE utf8mb3_spanish2_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8mb3_spanish2_ci NOT NULL,
  `apellidos` varchar(255) COLLATE utf8mb3_spanish2_ci NOT NULL,
  `clave` varchar(255) COLLATE utf8mb3_spanish2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish2_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `aulas`
--
ALTER TABLE `aulas`
  ADD PRIMARY KEY (`nombre`);

--
-- Indexes for table `cursos`
--
ALTER TABLE `cursos`
  ADD PRIMARY KEY (`nombre`);

--
-- Indexes for table `guardias`
--
ALTER TABLE `guardias`
  ADD PRIMARY KEY (`id`,`dia`,`hora`),
  ADD KEY `FK_horas` (`hora`),
  ADD KEY `FK_curso` (`curso`),
  ADD KEY `FK_aulas` (`aula`);

--
-- Indexes for table `horas`
--
ALTER TABLE `horas`
  ADD PRIMARY KEY (`nombre`);

--
-- Indexes for table `profesores`
--
ALTER TABLE `profesores`
  ADD PRIMARY KEY (`id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `guardias`
--
ALTER TABLE `guardias`
  ADD CONSTRAINT `FK_aulas` FOREIGN KEY (`aula`) REFERENCES `aulas` (`nombre`),
  ADD CONSTRAINT `FK_curso` FOREIGN KEY (`curso`) REFERENCES `cursos` (`nombre`),
  ADD CONSTRAINT `FK_horas` FOREIGN KEY (`hora`) REFERENCES `horas` (`nombre`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
