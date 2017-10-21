/*
SQLyog Community v12.3.2 (64 bit)
MySQL - 10.2.7-MariaDB : Database - task
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`task` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `task`;

/*Table structure for table `entrance_url` */

DROP TABLE IF EXISTS `entrance_url`;

CREATE TABLE `entrance_url` (
  `entrance_url_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `entrance_url_seq` bigint(20) DEFAULT NULL COMMENT '平台唯一',
  `entrance_url` varchar(512) DEFAULT NULL,
  `investment_platform` varchar(128) DEFAULT NULL,
  `worker_id` bigint(20) DEFAULT NULL,
  `worker_system_uuid` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`entrance_url_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10764 DEFAULT CHARSET=utf8;

/*Table structure for table `platform_account` */

DROP TABLE IF EXISTS `platform_account`;

CREATE TABLE `platform_account` (
  `platform_account_id` bigint(20) DEFAULT NULL,
  `platform_username` varchar(64) DEFAULT NULL,
  `platform_password` varchar(64) DEFAULT NULL,
  `investment_platform` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `worker` */

DROP TABLE IF EXISTS `worker`;

CREATE TABLE `worker` (
  `worker_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `worker_ip` varchar(64) DEFAULT NULL COMMENT 'worker的真实外网ip,是可以标识本worker的,非其使用的vpn后的出口ip',
  `bisz_table_id_start` bigint(20) DEFAULT NULL COMMENT '业务库各个表id起始数值',
  `entrance_url_id` bigint(20) DEFAULT NULL COMMENT 'url_start表中的id',
  `entrance_url_cnt` bigint(20) DEFAULT NULL COMMENT 'url个数',
  `worker_system_uuid` varchar(64) DEFAULT NULL COMMENT '当worker是拨号上网用户的时候，外网ip不定，所以可能要用cpu0的id来标识worker自己',
  PRIMARY KEY (`worker_id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
