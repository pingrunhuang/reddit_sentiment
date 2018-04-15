CREATE TABLE `sentiment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `unix` varchar(16) DEFAULT NULL,
  `title` varchar(4096) DEFAULT NULL,
  `sentiment` varchar(16) DEFAULT NULL,
  `category` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_title` (`unix`)
) ENGINE=InnoDB AUTO_INCREMENT=13107 DEFAULT CHARSET=utf8mb4;