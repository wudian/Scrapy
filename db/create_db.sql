DROP TABLE IF EXISTS project;
CREATE TABLE `project` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '项目id',
  `name` varchar(64) DEFAULT NULL COMMENT '项目名称',
  `logo_url` varchar(512) DEFAULT NULL COMMENT '项目logo',
  `product_description` varchar(1024) DEFAULT NULL COMMENT '项目描述',
  `company_name` varchar(64) DEFAULT NULL COMMENT '公司名称',
  `introduction` varchar(1024) DEFAULT NULL COMMENT '公司概述',
  `industry` varchar(32) DEFAULT NULL COMMENT '行业',
  `city` varchar(32) DEFAULT NULL COMMENT '所在地',
  `start_date` varchar(12) DEFAULT NULL COMMENT '成立时间',
  `site` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE (name),
  UNIQUE (company_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS company_member;
CREATE TABLE `company_member` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL COMMENT '姓名',
  `position` varchar(128) DEFAULT NULL COMMENT '职务',
  `experience` varchar(2048) DEFAULT NULL COMMENT '工作经历描述',
  `project_id` bigint(20) DEFAULT NULL COMMENT '所属项目 project表的id字段',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='公司成员' ;

DROP TABLE IF EXISTS financing_phase;
CREATE TABLE `financing_phase` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `phase` varchar(32) DEFAULT NULL COMMENT '轮次',
  `amount` varchar(32) DEFAULT NULL COMMENT '融资金额',
  `investor` varchar(128) DEFAULT NULL COMMENT '投资方',
  `date` varchar(16) DEFAULT NULL COMMENT '融资时间',
  `project_id` bigint(20) DEFAULT NULL COMMENT '所属项目 project表的id字段',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='融资经历（融资轮次列表）';

DROP TABLE IF EXISTS shareholder;
CREATE TABLE `shareholder` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL COMMENT '股东名字',
  `rate` varchar(64) DEFAULT NULL COMMENT '出资比例',
  `amount` varchar(256) DEFAULT NULL COMMENT '认缴出资',
  `time` varchar(32) DEFAULT NULL COMMENT '出资时间',
  `project_id` bigint(20) DEFAULT NULL COMMENT '所属项目 project表的id字段',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='股东信息' ;

