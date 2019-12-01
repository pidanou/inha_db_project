-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le :  Dim 01 déc. 2019 à 09:22
-- Version du serveur :  10.1.39-MariaDB
-- Version de PHP :  7.3.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `inha_db_project`
--

-- --------------------------------------------------------

--
-- Structure de la table `dbsettings`
--

CREATE TABLE `dbsettings` (
  `buffersize` int(11) NOT NULL,
  `spaceperuser` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `dbsettings`
--

INSERT INTO `dbsettings` (`buffersize`, `spaceperuser`) VALUES
(10, 50);

-- --------------------------------------------------------

--
-- Structure de la table `file`
--

CREATE TABLE `file` (
  `id` int(11) NOT NULL,
  `content` blob,
  `path` int(11) NOT NULL,
  `owner` int(11) NOT NULL,
  `edits` int(11) NOT NULL DEFAULT '0',
  `size` int(11) NOT NULL,
  `hotcold` enum('hot','cold') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `file`
--

INSERT INTO `file` (`id`, `content`, `path`, `owner`, `edits`, `size`, `hotcold`) VALUES
(0, 0x74686973206973206120746573742066696c650d0a616464656420746578740d0a616464656420746578740d0a616464656420746578740d0a616464656420746578740d0a616464656420746578740d0a616464656420746578740d0a616464656420746578740d0a616464656420746578740d0a61646465642074657874, 0, 2, 9, 127, 'hot');

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `user_type` tinyint(1) NOT NULL,
  `username` varchar(15) NOT NULL,
  `password` varchar(15) NOT NULL,
  `spaceleft` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`id`, `user_type`, `username`, `password`, `spaceleft`) VALUES
(1, 0, 'admin', 'admin', 50),
(2, 1, 'user', 'user', 50);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `file`
--
ALTER TABLE `file`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
