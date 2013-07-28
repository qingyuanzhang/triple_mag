-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.1.61-0ubuntu0.10.04.1


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema app_websupermarket
--

CREATE DATABASE IF NOT EXISTS app_websupermarket;
USE app_websupermarket;

--
-- Definition of table `app_websupermarket`.`engine_order`
--

DROP TABLE IF EXISTS `app_websupermarket`.`engine_order`;
CREATE TABLE  `app_websupermarket`.`engine_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `coustom_id` int(11) NOT NULL,
  `order_data` datetime DEFAULT NULL,
  `address_id` int(11) NOT NULL,
  `delivery_way` varchar(30) DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `is_recommand` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_order_d2b899d` (`coustom_id`),
  KEY `engine_order_4dec3e17` (`address_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `app_websupermarket`.`engine_order`
--

/*!40000 ALTER TABLE `engine_order` DISABLE KEYS */;
LOCK TABLES `engine_order` WRITE;
INSERT INTO `app_websupermarket`.`engine_order` VALUES  (1,1,'2012-05-31 19:36:32',39,'3','3',0),
 (2,1,'2012-05-31 19:36:32',39,'3','3',0),
 (3,1,'2012-05-31 19:36:32',39,'3','3',0),
 (4,1,'2012-05-31 19:36:32',39,'3','3',0),
 (5,1,'2012-05-31 19:40:19',39,'3','3',0),
 (6,1,'2012-05-31 19:57:01',39,'3','3',0),
 (7,1,'2012-05-31 20:03:02',39,'3','3',0),
 (8,1,'2012-05-31 20:03:02',39,'3','3',0);
UNLOCK TABLES;
/*!40000 ALTER TABLE `engine_order` ENABLE KEYS */;




/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
