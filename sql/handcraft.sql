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
INSERT INTO `user` VALUES ('1', 'yuhailong880106@gmail.com', 'handcraft', '18612189569', 'pbkdf2:sha1:1000$8Zv6wJQM$fe8d659f1de9dcbce584e68102209ec4d153b338', '0', '0'), ('8', 'yu.hailong@kuyun.com', '于海龙', '18612189569', 'pbkdf2:sha1:1000$8Zv6wJQM$fe8d659f1de9dcbce584e68102209ec4d153b338', '0', '0'), ('12', '616771221@qq.com', 'yhl', '18514530012', 'pbkdf2:sha1:1000$zT6Ot6TZ$77a7c81271884e08a1ddf0679ae6cba996a405bc', '0', '1'), ('13', '493121371@qq.com', 'abc', '18612189569', 'pbkdf2:sha1:1000$vNtIKA6J$e09efd442fd2ecef7baec082c0c1c56221025740', '2', '0'), ('14', '493121372@qq.com', 'ab', '18612189569', 'pbkdf2:sha1:1000$pYQIBIyt$54e58c8adf6efedbb943ff903e988734f6c10c11', '0', '1'), ('15', '493121373@qq.com', 'a', '18612189569', 'pbkdf2:sha1:1000$mdeRBonF$35716e043c51793d1233264a89257c596bcd14d3', '2', '0'), ('16', '49312373@qq.com', 'accc', '18612189569', 'pbkdf2:sha1:1000$tKj92N8q$0c3f3048dc499db7deb5241ce850b02a2b9f4e8d', '2', '1'), ('17', '123@qq.com', 'aaaa', '18612189569', 'pbkdf2:sha1:1000$GL7vNpcw$7f7dbed9abba11ebdd2b6ed447db0608f8a33e47', '1', '0'), ('18', 'aaa@qq.com', 'ccc', '18612189569', 'pbkdf2:sha1:1000$lzxSviDq$0e3ae7b1c7279b4a40c23448b933e8b3e287537b', '1', '1'), ('20', 'yuhailong88dd0106@gmail.com', 'yuhailongsss', '18612189569', 'pbkdf2:sha1:1000$3VoyxSRc$fcc0eb0cb324f22f7d40599b458182b069495b4a', '2', '0'), ('21', 'dfeq@qq.com', 'abcdd', '18612189569', 'pbkdf2:sha1:1000$jXlMrvMS$0b899074c8217af76b17afe29b50217bee36e8d0', '1', '1'), ('22', 'ss@qq.com', 'ss', '18612189569', 'pbkdf2:sha1:1000$bRqvQBMy$e78c916bc31b0753ed126bb2e313156a510bf3fa', '0', '0'), ('23', 'ddrae@qq.com', 'dre', '18612189569', 'pbkdf2:sha1:1000$elOvM1dt$76863fbd44bd32398aa89594e9e13447fae1cc28', '1', '0'), ('24', 'ddr2ae@qq.com', 'dre3', '18612189569', 'pbkdf2:sha1:1000$rmEyUKG3$f58966eef87132ba6557ac52deeacaf89e9e8ea2', '1', '0'), ('25', 'sar2W@qq.com', 'dder', '18612189569', 'pbkdf2:sha1:1000$8kv7OJmw$97da67a000b7be7939d2f68e218db686bd278593', '0', '1'), ('26', 'dddd@qq.com', 'edddd', '18612189569', 'pbkdf2:sha1:1000$DrkF4cAq$e4fba16ea2c4ce84218cb0a03f10672b7d996b2c', '1', '1'), ('27', 'se@qq.com', 'admin', '18612189569', 'pbkdf2:sha1:1000$2CVuMVRW$abd8af000799b8fb26ea57ff9bd0ff6bd19cf49d', '1', '0'), ('28', 'ser@qq.com', 'ser', '18612189569', 'pbkdf2:sha1:1000$EoexaBUC$abbc1f61f6f36424b96c31fd50e6d37721fd3b22', '1', '1'), ('30', '3sder@qq.com', 'ser3d', '18612189569', 'pbkdf2:sha1:1000$IP95eKSr$dfdfa7472bda518a4621b38f9320b82017518e72', '2', '0'), ('31', '3sdfer@qq.com', 'ser3dd', '18612189569', 'pbkdf2:sha1:1000$1vypaNBX$677b36cca286d3c1abc6bd159ab1a7e508696c64', '2', '0'), ('33', 'xxx@11.com', 'xxxx', '18612189569', 'pbkdf2:sha1:1000$YlJz7hOS$1ab2b1aafa2260231188d07928769d3659127d6d', '1', '0'), ('34', 'xxxx@11.com', 'xxxxx', '18612189569', 'pbkdf2:sha1:1000$KuSm9CC0$595db27a32cdbc837a60d96f37cfa1a72bf49bfd', '1', '0'), ('35', 'xxxxx@11.com', 'xxxxxx', '18612189569', 'pbkdf2:sha1:1000$LZppzcZj$0724b6f7498821dafc4ac024029cc07e6ab37ccc', '0', '0');
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
