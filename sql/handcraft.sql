/*
 Navicat Premium Data Transfer

 Source Server         : flask
 Source Server Type    : MySQL
 Source Server Version : 50627
 Source Host           : 192.168.200.125
 Source Database       : handcraft

 Target Server Type    : MySQL
 Target Server Version : 50627
 File Encoding         : utf-8

 Date: 10/14/2016 14:18:31 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `group`
-- ----------------------------
DROP TABLE IF EXISTS `group`;
CREATE TABLE `group` (
  `id` int(2) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `comment` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `group`
-- ----------------------------
BEGIN;
INSERT INTO `group` VALUES ('1', 'ops', null), ('2', 'test', null);
COMMIT;

-- ----------------------------
--  Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(64) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `role` varchar(1) DEFAULT NULL,
  `active` varchar(1) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_email` (`email`),
  UNIQUE KEY `ix_user_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `user`
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES ('1', 'yuhailong880106@gmail.com', 'handcraft', '*************', 'pbkdf2:sha1:1000$8Zv6wJQM$fe8d659f1de9dcbce584e68102209ec4d153b338', '0', '0');
COMMIT;

-- ----------------------------
--  Table structure for `user_group`
-- ----------------------------
DROP TABLE IF EXISTS `user_group`;
CREATE TABLE `user_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(2) DEFAULT NULL,
  `group_id` int(2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`) USING BTREE,
  KEY `user_6340c63c` (`user_id`) USING BTREE,
  KEY `group_d9f50f95` (`group_id`) USING BTREE,
  CONSTRAINT `group_id_refs_id_5a8d9fc9` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`),
  CONSTRAINT `user_id_refs_id_fb2280e7` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `user_group`
-- ----------------------------
BEGIN;
INSERT INTO `user_group` VALUES ('1', '35', '1'), ('2', '35', '2');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
