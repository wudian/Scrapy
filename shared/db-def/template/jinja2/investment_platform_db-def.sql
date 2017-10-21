-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 10.253.115.203    Database: investment_platform_db
-- ------------------------------------------------------
-- Server version	5.5.5-10.1.28-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`investment_platform_db{{bisz_table_id_start}}` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `investment_platform_db{{bisz_table_id_start}}`;
--
-- Table structure for table `chandashi_rank`
--

DROP TABLE IF EXISTS `chandashi_rank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `change_info`
--

DROP TABLE IF EXISTS `change_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `change_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `change_date` varchar(32) DEFAULT NULL COMMENT '变更时间',
  `change_type` varchar(64) DEFAULT NULL COMMENT '变更类型',
  `before_change` varchar(256) DEFAULT NULL COMMENT '变更前',
  `after_change` varchar(256) DEFAULT NULL COMMENT '变更后',
  `project_id` int(20) DEFAULT NULL COMMENT '所属项目在project表里的id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `company_member`
--

DROP TABLE IF EXISTS `company_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company_member` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL COMMENT '姓名',
  `position` varchar(128) DEFAULT NULL COMMENT '职务',
  `experience` varchar(2048) DEFAULT NULL COMMENT '工作经历描述',
  `project_id` bigint(20) DEFAULT NULL COMMENT '所属项目 project表的id字段',
  `investment_platform` varchar(128) DEFAULT NULL,
  `delflag` enum('Y','N') DEFAULT 'N' COMMENT '删除标志',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建用户',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改用户',
  `created` datetime DEFAULT NULL COMMENT '新建时间',
  `updated` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT={{bisz_table_id_start}} DEFAULT CHARSET=utf8 COMMENT='公司成员';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `financing_phase`
--

DROP TABLE IF EXISTS `financing_phase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `financing_phase` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `phase` varchar(32) DEFAULT NULL COMMENT '轮次',
  `amount` varchar(32) DEFAULT NULL COMMENT '融资金额',
  `investor` varchar(128) DEFAULT NULL COMMENT '投资方',
  `date` varchar(16) DEFAULT NULL COMMENT '融资时间',
  `project_id` bigint(20) DEFAULT NULL COMMENT '所属项目 project表的id字段',
  `investment_platform` varchar(128) DEFAULT NULL,
  `delflag` enum('Y','N') DEFAULT 'N' COMMENT '删除标志',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建用户',
  `modifier` varchar(64) DEFAULT NULL COMMENT '修改用户',
  `created` datetime DEFAULT NULL COMMENT '新建时间',
  `updated` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT={{bisz_table_id_start}} DEFAULT CHARSET=utf8 COMMENT='融资经历（融资轮次列表）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `industry_info`
--

DROP TABLE IF EXISTS `industry_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `industry_info` (
  `project_id` int(20) NOT NULL COMMENT '所属项目在project表里的id',
  `corp_name` varchar(64) DEFAULT NULL COMMENT '公司全称',
  `reg_capital` varchar(32) DEFAULT NULL COMMENT '注册资本',
  `corp_rep` varchar(32) DEFAULT NULL COMMENT '法人代表',
  `reg_date` varchar(16) DEFAULT NULL COMMENT '注册时间',
  PRIMARY KEY (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ips_user`
--

DROP TABLE IF EXISTS `ips_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ips_user` (
  `id` varchar(64) NOT NULL,
  `area_name` varchar(128) DEFAULT NULL COMMENT '地区名称',
  `area_code` varchar(128) DEFAULT NULL COMMENT '区号',
  `name` varchar(128) DEFAULT NULL COMMENT '账号名称',
  `passwd` varchar(128) DEFAULT NULL COMMENT '密码',
  `email` varchar(128) DEFAULT NULL COMMENT '帐号Email',
  `mobile` varchar(64) DEFAULT NULL COMMENT '帐号手机号',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '状态0正常，1锁定 2 待激活',
  `retry` int(11) DEFAULT '0' COMMENT '重试次数',
  `lock_time` datetime DEFAULT NULL COMMENT '锁定时间',
  `delflag` enum('Y','N') NOT NULL DEFAULT 'N' COMMENT '删除标志',
  `created` datetime DEFAULT NULL COMMENT '新建时间',
  `creator` varchar(64) DEFAULT NULL,
  `updated` datetime DEFAULT NULL COMMENT '更新时间',
  `modifier` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `AK_Key_2` (`name`),
  KEY `AK_Key_3` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
  `founder` varchar(64) DEFAULT NULL COMMENT '应放在公司成员表中',
  `founder_description` varchar(1024) DEFAULT NULL COMMENT '创始人简介 应放在公司成员表中',
  `modifier` varchar(64) DEFAULT NULL,
  `created` datetime DEFAULT NULL COMMENT '新建时间',
  `updated` datetime DEFAULT NULL COMMENT '更新时间',
  `creator` varchar(64) DEFAULT NULL,
  `address` varchar(128) DEFAULT NULL COMMENT '详细地址',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_name_invtpltfm` (`name`,`investment_platform`)
) ENGINE=InnoDB AUTO_INCREMENT={{bisz_table_id_start}} DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seochinaz_rank`
--

DROP TABLE IF EXISTS `seochinaz_rank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shareholder_info`
--

DROP TABLE IF EXISTS `shareholder_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shareholder_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `share_type` varchar(32) DEFAULT NULL COMMENT '法人类型',
  `share_name` varchar(32) DEFAULT NULL COMMENT '法人名称',
  `project_id` int(20) DEFAULT NULL COMMENT '所属项目在project表里的id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `staff_info`
--

DROP TABLE IF EXISTS `staff_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `staff_pos` varchar(32) DEFAULT NULL COMMENT '人员职位',
  `staff_name` varchar(32) DEFAULT NULL COMMENT '人员姓名',
  `project_id` int(20) DEFAULT NULL COMMENT '所属项目在project表里的id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-14 10:59:23
