/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50548
Source Host           : localhost:3306
Source Database       : smopsv7

Target Server Type    : MYSQL
Target Server Version : 50548
File Encoding         : 65001

Date: 2016-07-18 15:42:45
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES ('1', 'Can add permission', '1', 'add_permission');
INSERT INTO `auth_permission` VALUES ('2', 'Can change permission', '1', 'change_permission');
INSERT INTO `auth_permission` VALUES ('3', 'Can delete permission', '1', 'delete_permission');
INSERT INTO `auth_permission` VALUES ('4', 'Can add group', '2', 'add_group');
INSERT INTO `auth_permission` VALUES ('5', 'Can change group', '2', 'change_group');
INSERT INTO `auth_permission` VALUES ('6', 'Can delete group', '2', 'delete_group');
INSERT INTO `auth_permission` VALUES ('10', 'Can add content type', '4', 'add_contenttype');
INSERT INTO `auth_permission` VALUES ('11', 'Can change content type', '4', 'change_contenttype');
INSERT INTO `auth_permission` VALUES ('12', 'Can delete content type', '4', 'delete_contenttype');
INSERT INTO `auth_permission` VALUES ('13', 'Can add session', '5', 'add_session');
INSERT INTO `auth_permission` VALUES ('14', 'Can change session', '5', 'change_session');
INSERT INTO `auth_permission` VALUES ('15', 'Can delete session', '5', 'delete_session');
INSERT INTO `auth_permission` VALUES ('16', 'Can add 用户表', '6', 'add_userprofile');
INSERT INTO `auth_permission` VALUES ('17', 'Can change 用户表', '6', 'change_userprofile');
INSERT INTO `auth_permission` VALUES ('18', 'Can delete 用户表', '6', 'delete_userprofile');
INSERT INTO `auth_permission` VALUES ('19', 'Can add 主机', '7', 'add_host');
INSERT INTO `auth_permission` VALUES ('20', 'Can change 主机', '7', 'change_host');
INSERT INTO `auth_permission` VALUES ('21', 'Can delete 主机', '7', 'delete_host');
INSERT INTO `auth_permission` VALUES ('22', 'Can add 系统用户', '8', 'add_sys_user');
INSERT INTO `auth_permission` VALUES ('23', 'Can change 系统用户', '8', 'change_sys_user');
INSERT INTO `auth_permission` VALUES ('24', 'Can delete 系统用户', '8', 'delete_sys_user');
INSERT INTO `auth_permission` VALUES ('25', 'Can add 白名单操作', '9', 'add_whitelist_event');
INSERT INTO `auth_permission` VALUES ('26', 'Can change 白名单操作', '9', 'change_whitelist_event');
INSERT INTO `auth_permission` VALUES ('27', 'Can delete 白名单操作', '9', 'delete_whitelist_event');
INSERT INTO `auth_permission` VALUES ('28', 'Can add SVN账户', '10', 'add_svn_user');
INSERT INTO `auth_permission` VALUES ('29', 'Can change SVN账户', '10', 'change_svn_user');
INSERT INTO `auth_permission` VALUES ('30', 'Can delete SVN账户', '10', 'delete_svn_user');
INSERT INTO `auth_permission` VALUES ('31', 'Can add 业务', '11', 'add_business');
INSERT INTO `auth_permission` VALUES ('32', 'Can change 业务', '11', 'change_business');
INSERT INTO `auth_permission` VALUES ('33', 'Can delete 业务', '11', 'delete_business');
INSERT INTO `auth_permission` VALUES ('34', 'Can add business_host', '12', 'add_business_host');
INSERT INTO `auth_permission` VALUES ('35', 'Can change business_host', '12', 'change_business_host');
INSERT INTO `auth_permission` VALUES ('36', 'Can delete business_host', '12', 'delete_business_host');
INSERT INTO `auth_permission` VALUES ('37', 'Can add 功能模块', '13', 'add_module');
INSERT INTO `auth_permission` VALUES ('38', 'Can change 功能模块', '13', 'change_module');
INSERT INTO `auth_permission` VALUES ('39', 'Can delete 功能模块', '13', 'delete_module');
INSERT INTO `auth_permission` VALUES ('40', 'Can add 版本发布事件', '14', 'add_publish_event');
INSERT INTO `auth_permission` VALUES ('41', 'Can change 版本发布事件', '14', 'change_publish_event');
INSERT INTO `auth_permission` VALUES ('42', 'Can delete 版本发布事件', '14', 'delete_publish_event');
INSERT INTO `auth_permission` VALUES ('43', 'Can add log entry', '15', 'add_logentry');
INSERT INTO `auth_permission` VALUES ('44', 'Can change log entry', '15', 'change_logentry');
INSERT INTO `auth_permission` VALUES ('45', 'Can delete log entry', '15', 'delete_logentry');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for core_business
-- ----------------------------
DROP TABLE IF EXISTS `core_business`;
CREATE TABLE `core_business` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `directory` varchar(255) NOT NULL,
  `svn_dir` varchar(255) NOT NULL,
  `running_user` varchar(20) NOT NULL,
  `svn_user_id` int(11) NOT NULL,
  `current_version` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `core_business_svn_user_id_c8b123dd_uniq` (`svn_user_id`,`name`),
  KEY `core_business_090bc91e` (`svn_user_id`),
  CONSTRAINT `core_business_svn_user_id_24b70000_fk_core_svn_user_id` FOREIGN KEY (`svn_user_id`) REFERENCES `core_svn_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of core_business
-- ----------------------------
INSERT INTO `core_business` VALUES ('1', 'Admin', '0', '2016-07-12 17:41:11', '/home/data/www/', '/sm8/Admin/', 'nginx', '1', '1');

-- ----------------------------
-- Table structure for core_business_host
-- ----------------------------
DROP TABLE IF EXISTS `core_business_host`;
CREATE TABLE `core_business_host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_version` varchar(100) NOT NULL,
  `business_id` int(11) NOT NULL,
  `host_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_business_host_business_id_6fb7b1e2_fk_core_business_id` (`business_id`),
  KEY `core_business_host_8396f175` (`host_id`),
  CONSTRAINT `core_business_host_host_id_7aedc7da_fk_core_host_id` FOREIGN KEY (`host_id`) REFERENCES `core_host` (`id`),
  CONSTRAINT `core_business_host_business_id_6fb7b1e2_fk_core_business_id` FOREIGN KEY (`business_id`) REFERENCES `core_business` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of core_business_host
-- ----------------------------
INSERT INTO `core_business_host` VALUES ('1', '1', '1', '1');

-- ----------------------------
-- Table structure for core_host
-- ----------------------------
DROP TABLE IF EXISTS `core_host`;
CREATE TABLE `core_host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `desc` varchar(255) DEFAULT NULL,
  `ipaddr` char(39) NOT NULL,
  `prefix` int(11) NOT NULL,
  `port` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `add_time` datetime NOT NULL,
  `modify_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of core_host
-- ----------------------------
INSERT INTO `core_host` VALUES ('1', 'host1', '', '1.2.3.136', '24', '22', '0', '2016-07-08 12:57:31', '2016-07-08 12:57:34');
INSERT INTO `core_host` VALUES ('4', 'SM8_SVN', '', '1.2.3.152', '32', '22', '0', '2016-07-08 16:21:29', '2016-07-08 16:21:29');

-- ----------------------------
-- Table structure for core_module
-- ----------------------------
DROP TABLE IF EXISTS `core_module`;
CREATE TABLE `core_module` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `desc` varchar(255) DEFAULT NULL,
  `parent` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1013 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of core_module
-- ----------------------------
INSERT INTO `core_module` VALUES ('1', 'whitlist_mgt', '白名单管理', '0');
INSERT INTO `core_module` VALUES ('2', 'user_mgt', '用户管理', '0');
INSERT INTO `core_module` VALUES ('3', 'host_mgt', '主机管理', '0');
INSERT INTO `core_module` VALUES ('4', 'publish_mgt', '版本管理', '0');
INSERT INTO `core_module` VALUES ('5', 'business_mgt', '业务管理', '0');
INSERT INTO `core_module` VALUES ('100', 'module_mgt', '模块管理', '0');
INSERT INTO `core_module` VALUES ('1001', 'whitelist', '白名单', '1');
INSERT INTO `core_module` VALUES ('1002', 'whitelist_event', '操作记录', '1');
INSERT INTO `core_module` VALUES ('1003', 'ywuser', '运维用户', '2');
INSERT INTO `core_module` VALUES ('1004', 'sysuser', '系统用户', '2');
INSERT INTO `core_module` VALUES ('1005', 'svnuser', 'SVN用户', '2');
INSERT INTO `core_module` VALUES ('1006', 'ver_publish', '发布版本', '4');
INSERT INTO `core_module` VALUES ('1007', 'ver_rollback', '版本回滚', '4');
INSERT INTO `core_module` VALUES ('1008', 'ver_event', '发布记录', '4');
INSERT INTO `core_module` VALUES ('1009', 'businesslist', '业务列表', '5');
INSERT INTO `core_module` VALUES ('1010', 'hostlist', '主机列表', '3');
INSERT INTO `core_module` VALUES ('1011', 'ver_business', '业务状态', '4');
INSERT INTO `core_module` VALUES ('1012', 'modulelist', '模块列表', '100');

-- ----------------------------
-- Table structure for core_module_user
-- ----------------------------
DROP TABLE IF EXISTS `core_module_user`;
CREATE TABLE `core_module_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `module_id` int(11) NOT NULL,
  `userprofile_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_module_user_module_id_d6cc062f_uniq` (`module_id`,`userprofile_id`),
  KEY `core_module_user_userprofile_id_babc8269_fk_core_userprofile_id` (`userprofile_id`),
  CONSTRAINT `core_module_user_userprofile_id_babc8269_fk_core_userprofile_id` FOREIGN KEY (`userprofile_id`) REFERENCES `core_userprofile` (`id`),
  CONSTRAINT `core_module_user_module_id_5fc439c4_fk_core_module_id` FOREIGN KEY (`module_id`) REFERENCES `core_module` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of core_module_user
-- ----------------------------
INSERT INTO `core_module_user` VALUES ('1', '1', '1');
INSERT INTO `core_module_user` VALUES ('2', '2', '1');
INSERT INTO `core_module_user` VALUES ('3', '3', '1');
INSERT INTO `core_module_user` VALUES ('4', '4', '1');
INSERT INTO `core_module_user` VALUES ('5', '5', '1');
INSERT INTO `core_module_user` VALUES ('22', '100', '1');
INSERT INTO `core_module_user` VALUES ('8', '1001', '1');
INSERT INTO `core_module_user` VALUES ('9', '1002', '1');
INSERT INTO `core_module_user` VALUES ('10', '1003', '1');
INSERT INTO `core_module_user` VALUES ('11', '1004', '1');
INSERT INTO `core_module_user` VALUES ('12', '1005', '1');
INSERT INTO `core_module_user` VALUES ('13', '1006', '1');
INSERT INTO `core_module_user` VALUES ('14', '1007', '1');
INSERT INTO `core_module_user` VALUES ('15', '1008', '1');
INSERT INTO `core_module_user` VALUES ('16', '1009', '1');
INSERT INTO `core_module_user` VALUES ('17', '1010', '1');
INSERT INTO `core_module_user` VALUES ('18', '1011', '1');
INSERT INTO `core_module_user` VALUES ('23', '1012', '1');

-- ----------------------------
-- Table structure for core_publish_event
-- ----------------------------
DROP TABLE IF EXISTS `core_publish_event`;
CREATE TABLE `core_publish_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operator` varchar(20) NOT NULL,
  `ipaddr` char(39) NOT NULL,
  `original_ver` varchar(100) NOT NULL,
  `current_ver` varchar(100) NOT NULL,
  `rollback_ver` varchar(100) DEFAULT NULL,
  `status` int(11) NOT NULL,
  `desc` varchar(255) NOT NULL,
  `result` varchar(255) DEFAULT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of core_publish_event
-- ----------------------------

-- ----------------------------
-- Table structure for core_svn_user
-- ----------------------------
DROP TABLE IF EXISTS `core_svn_user`;
CREATE TABLE `core_svn_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `host_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `core_svn_user_host_id_d86713c9_uniq` (`host_id`,`username`),
  CONSTRAINT `core_svn_user_host_id_f3c0aebd_fk_core_host_id` FOREIGN KEY (`host_id`) REFERENCES `core_host` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of core_svn_user
-- ----------------------------
INSERT INTO `core_svn_user` VALUES ('1', '', '', '', '4');

-- ----------------------------
-- Table structure for core_sys_user
-- ----------------------------
DROP TABLE IF EXISTS `core_sys_user`;
CREATE TABLE `core_sys_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `host_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_sys_user_host_id_5ed1b1d6_uniq` (`host_id`,`user_id`),
  KEY `core_sys_user_e8701ad4` (`user_id`),
  CONSTRAINT `core_sys_user_user_id_d8875e5e_fk_core_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `core_userprofile` (`id`),
  CONSTRAINT `core_sys_user_host_id_041c14f8_fk_core_host_id` FOREIGN KEY (`host_id`) REFERENCES `core_host` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of core_sys_user
-- ----------------------------
INSERT INTO `core_sys_user` VALUES ('1', 'root', 'abc.123', '1', '1');

-- ----------------------------
-- Table structure for core_userprofile
-- ----------------------------
DROP TABLE IF EXISTS `core_userprofile`;
CREATE TABLE `core_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `username` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(30) DEFAULT NULL,
  `desc` varchar(255) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `add_time` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of core_userprofile
-- ----------------------------
INSERT INTO `core_userprofile` VALUES ('1', 'pbkdf2_sha256$24000$gJqPi8DykGtC$qXrhX1ow0aSIL1EGrIaojGR17iQXMPRrLsrVfvDiMWA=', '2016-07-18 15:35:40', 'admin', 'Admin', 'admin@localhost.local', '', '0', '2016-07-04 17:34:16', '1', '1');

-- ----------------------------
-- Table structure for core_whitelist_event
-- ----------------------------
DROP TABLE IF EXISTS `core_whitelist_event`;
CREATE TABLE `core_whitelist_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operator` varchar(20) NOT NULL,
  `ipaddr` char(39) NOT NULL,
  `prefix` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `src_ip` char(39) NOT NULL,
  `datetime` datetime NOT NULL,
  `operation` varchar(10) NOT NULL,
  `desc` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of core_whitelist_event
-- ----------------------------
INSERT INTO `core_whitelist_event` VALUES ('9', 'Admin', '1.3.3.4', '32', '0', '1.2.3.120', '2016-07-14 13:53:24', '添加', '这是一个中文注释');

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_core_userprofile_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_core_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `core_userprofile` (`id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES ('15', 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES ('2', 'auth', 'group');
INSERT INTO `django_content_type` VALUES ('1', 'auth', 'permission');
INSERT INTO `django_content_type` VALUES ('4', 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES ('11', 'core', 'business');
INSERT INTO `django_content_type` VALUES ('12', 'core', 'business_host');
INSERT INTO `django_content_type` VALUES ('7', 'core', 'host');
INSERT INTO `django_content_type` VALUES ('13', 'core', 'module');
INSERT INTO `django_content_type` VALUES ('14', 'core', 'publish_event');
INSERT INTO `django_content_type` VALUES ('10', 'core', 'svn_user');
INSERT INTO `django_content_type` VALUES ('8', 'core', 'sys_user');
INSERT INTO `django_content_type` VALUES ('6', 'core', 'userprofile');
INSERT INTO `django_content_type` VALUES ('9', 'core', 'whitelist_event');
INSERT INTO `django_content_type` VALUES ('5', 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES ('1', 'contenttypes', '0001_initial', '2016-07-13 08:37:10');
INSERT INTO `django_migrations` VALUES ('2', 'contenttypes', '0002_remove_content_type_name', '2016-07-13 08:37:10');
INSERT INTO `django_migrations` VALUES ('3', 'auth', '0001_initial', '2016-07-13 08:37:10');
INSERT INTO `django_migrations` VALUES ('4', 'auth', '0002_alter_permission_name_max_length', '2016-07-13 08:37:10');
INSERT INTO `django_migrations` VALUES ('5', 'auth', '0003_alter_user_email_max_length', '2016-07-13 08:37:10');
INSERT INTO `django_migrations` VALUES ('6', 'auth', '0004_alter_user_username_opts', '2016-07-13 08:37:10');
INSERT INTO `django_migrations` VALUES ('7', 'auth', '0005_alter_user_last_login_null', '2016-07-13 08:37:10');
INSERT INTO `django_migrations` VALUES ('8', 'auth', '0006_require_contenttypes_0002', '2016-07-13 08:37:10');
INSERT INTO `django_migrations` VALUES ('9', 'auth', '0007_alter_validators_add_error_messages', '2016-07-13 08:37:10');
INSERT INTO `django_migrations` VALUES ('10', 'core', '0001_initial', '2016-07-13 08:37:11');
INSERT INTO `django_migrations` VALUES ('11', 'core', '0002_auto_20160713_1403', '2016-07-13 08:37:12');
INSERT INTO `django_migrations` VALUES ('12', 'core', '0003_auto_20160713_1412', '2016-07-13 08:37:12');
INSERT INTO `django_migrations` VALUES ('13', 'core', '0004_auto_20160713_1637', '2016-07-13 08:37:12');
INSERT INTO `django_migrations` VALUES ('14', 'sessions', '0001_initial', '2016-07-13 08:37:12');
INSERT INTO `django_migrations` VALUES ('15', 'core', '0005_auto_20160713_1639', '2016-07-13 08:39:56');
INSERT INTO `django_migrations` VALUES ('16', 'core', '0006_auto_20160713_1640', '2016-07-13 08:40:33');
INSERT INTO `django_migrations` VALUES ('17', 'admin', '0001_initial', '2016-07-14 18:55:49');
INSERT INTO `django_migrations` VALUES ('18', 'admin', '0002_logentry_remove_auto_add', '2016-07-14 18:55:49');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('2wkcglug5lx4t6ootycj8by88cvjvsza', 'NDVmNDJlODRkNDA4Y2E2YjgzNDBjNWFiNTdkMmIxZmYyZTU4NTIyZDp7Il9hdXRoX3VzZXJfaGFzaCI6ImE3ODUyZGI2MGI1YzNlNjk2OTY5OTc3MTIwZDg2ZmYwMDZkNzQzNWUiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2016-07-19 11:33:03');
INSERT INTO `django_session` VALUES ('2xuo8dzreotgmdiga7r98udznso7p7uc', 'OTVmY2UxNTlkYjZlMGU0OTRjOTJiYmE1YjMzMzM3NTAwM2IzMWY0Mzp7Il9hdXRoX3VzZXJfaGFzaCI6IjFkZGZjNmQwNThjOTg3MjgwNjkxZWUwNDBmOTQ1MjllMGMxNGVhOGMiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2016-08-01 15:35:40');
INSERT INTO `django_session` VALUES ('9bf34qnlw4378fx4jzvankt2sv8kptt8', 'N2Y2MjA2YjZkODE4NDBkMDVhMjI4Zjk2NjA2NGY0NWI0MmI1OWI2MTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiZTBkOGNhYjAwMGIyZDNiN2M2MWExMDkxZDdiMWNkMjU0NDY4NTMwMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2016-07-29 10:30:24');
INSERT INTO `django_session` VALUES ('x7ywoorazcotjtxfa1c737rw4r95rsmm', 'NDBjMjMwNmY1MDA3ZDQ3MGIyMmM3OWU0NzQxYmFhYWE3YTZlNTU2Zjp7Il9hdXRoX3VzZXJfaGFzaCI6IjkyYzNhMTRmOGI0ZTlhNDZlMWRmY2VmMDgxZTFiNjgyZDExOTJkYzQiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2016-07-19 12:01:30');
