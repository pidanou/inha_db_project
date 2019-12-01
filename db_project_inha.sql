
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `dbsettings` (
  `name` varchar(10) NOT NULL,
  `value` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `dbsettings` (`name`, `value`) VALUES
('buffersize', 30),
('spaceallow', 100);



CREATE TABLE `file` (
  `id` int(11) NOT NULL,
  `content` blob NOT NULL,
  `path` text NOT NULL,
  `owner_id` int(11) NOT NULL,
  `edits` int(11) NOT NULL,
  `size` int(11) NOT NULL,
  `hotcold` enum('hot','cold') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(15) NOT NULL,
  `password` varchar(15) NOT NULL,
  `user_type` tinyint(4) NOT NULL,
  `spaceleft` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `user` (`id`, `username`, `password`, `user_type`, `spaceleft`) VALUES
(1, 'admin', 'admin', 0, 100),
(2, 'user', 'user', 1, 100);


ALTER TABLE `file`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_owner` (`owner_id`);


ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `file`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

ALTER TABLE `file`
  ADD CONSTRAINT `fk_owner` FOREIGN KEY (`owner_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;
