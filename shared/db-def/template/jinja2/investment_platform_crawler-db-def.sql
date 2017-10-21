/*
SQLyog Community v12.3.2 (64 bit)
MySQL - 10.1.28-MariaDB : Database - investment_platform_db{{bisz_table_id_start}}
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`investment_platform_db{{bisz_table_id_start}}` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `investment_platform_db{{bisz_table_id_start}}`;

/*Table structure for table `chandashi_rank` */

DROP TABLE IF EXISTS `chandashi_rank`;

CREATE TABLE `chandashi_rank` (
  `project_id` int(20) NOT NULL COMMENT '项目编号',
  `name` varchar(64) DEFAULT NULL COMMENT '关键词',
  `appname` varchar(128) DEFAULT NULL COMMENT '应用全称',
  `hotindex` int(32) DEFAULT NULL COMMENT '关键词热度',
  `ranktype1` varchar(64) DEFAULT NULL COMMENT '分类',
  `rank1` varchar(64) DEFAULT NULL COMMENT '分类排名',
  `ranktype2` varchar(64) DEFAULT NULL COMMENT '总榜',
  `rank2` varchar(64) DEFAULT NULL COMMENT '总榜排名',
  PRIMARY KEY (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT={{bisz_table_id_start}}  DEFAULT CHARSET=utf8;

/*Table structure for table `company_member` */

DROP TABLE IF EXISTS `company_member`;

CREATE TABLE `company_member` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL COMMENT '姓名',
  `position` varchar(64) DEFAULT NULL COMMENT '职务',
  `experience` varchar(10240) DEFAULT NULL COMMENT '工作经历描述',
  `project_id` bigint(20) DEFAULT NULL COMMENT '所属项目 project表的id字段',
  `investment_platform` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT={{bisz_table_id_start}}  DEFAULT CHARSET=utf8 COMMENT='公司成员';

/*Table structure for table `financing_phase` */

DROP TABLE IF EXISTS `financing_phase`;

CREATE TABLE `financing_phase` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `phase` varchar(32) DEFAULT NULL COMMENT '轮次',
  `amount` varchar(32) DEFAULT NULL COMMENT '融资金额',
  `investor` varchar(96) DEFAULT NULL COMMENT '投资方',
  `date` varchar(16) DEFAULT NULL COMMENT '融资时间',
  `project_id` bigint(20) DEFAULT NULL COMMENT '所属项目 project表的id字段',
  `investment_platform` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT={{bisz_table_id_start}}  DEFAULT CHARSET=utf8 COMMENT='融资经历（融资轮次列表）';

/*Table structure for table `project` */

DROP TABLE IF EXISTS `project`;

CREATE TABLE `project` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `logo_url` varchar(512) DEFAULT NULL COMMENT 'logo',
  `name` varchar(64) DEFAULT NULL COMMENT '项目名称',
  `introduction` varchar(1024) DEFAULT NULL COMMENT '项目概述',
  `product_description` varchar(1024) DEFAULT NULL COMMENT '产品描述',
  `advantage` varchar(1024) DEFAULT NULL COMMENT '项目优势',
  `achievement` varchar(1024) DEFAULT NULL COMMENT '取得成绩',
  `industry` varchar(32) DEFAULT NULL COMMENT '行业',
  `financing_phase` varchar(32) DEFAULT NULL COMMENT '融资轮次',
  `raised_fund` varchar(20) DEFAULT NULL COMMENT '已融资额度\n',
  `city` varchar(32) DEFAULT NULL COMMENT '所在地',
  `company_name` varchar(64) DEFAULT NULL COMMENT '公司名称',
  `start_date` varchar(12) DEFAULT NULL COMMENT '成立时间',
  `investment_platform` varchar(128) DEFAULT NULL COMMENT '从哪个网站抓取的',
  `picture_set` varchar(1024) DEFAULT NULL COMMENT '详情图片，多个图片以; 分割',
  `site` varchar(64) DEFAULT NULL,
  `delflag` enum('Y','N') DEFAULT 'N' COMMENT '删除标志',
  `founder` varchar(64) DEFAULT NULL,
  `founder_description` varchar(1024) DEFAULT NULL COMMENT '创始人简介',
  `modifier` varchar(64) DEFAULT NULL,
  `created` datetime DEFAULT NULL COMMENT '新建时间',
  `updated` datetime DEFAULT NULL COMMENT '更新时间',
  `creator` varchar(64) DEFAULT NULL,
  `address` varchar(128) DEFAULT NULL COMMENT '详细地址',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_name_invtpltfm` (`name`,`investment_platform`)
) ENGINE=InnoDB AUTO_INCREMENT={{bisz_table_id_start}}  DEFAULT CHARSET=utf8;

/*Table structure for table `seochinaz_rank` */

DROP TABLE IF EXISTS `seochinaz_rank`;

CREATE TABLE `seochinaz_rank` (
  `project_id` bigint(20) NOT NULL,
  `site` varchar(255) NOT NULL,
  `alexaRank` varchar(11) DEFAULT NULL,
  `baiduWeight` varchar(11) DEFAULT NULL,
  `baiduTraffic` varchar(11) DEFAULT NULL,
  `baiduRecordsNumber` varchar(11) DEFAULT NULL,
  `oneMonthRecordsNumber` varchar(11) DEFAULT NULL,
  `baiduIndexNumber` varchar(11) DEFAULT NULL,
  `baiduTheChainNumber` varchar(11) DEFAULT NULL,
  `keyWordNumber` varchar(11) DEFAULT NULL,
  `alexaTrafficRank` varchar(11) DEFAULT NULL,
  `prValue` varchar(11) DEFAULT NULL,
  `googleRecordsNumber` varchar(11) DEFAULT NULL,
  `googleTheChainNumber` varchar(11) DEFAULT NULL,
  `tllSiteRecordsNumber` varchar(11) DEFAULT NULL,
  `tllSiteTheChainNumber` varchar(11) DEFAULT NULL,
  `sougouRecordsNumber` varchar(11) DEFAULT NULL,
  `theChainNumber` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT={{bisz_table_id_start}}  DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
