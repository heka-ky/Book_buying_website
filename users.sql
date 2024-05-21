/*
 Navicat Premium Data Transfer

 Source Server         : users
 Source Server Type    : MySQL
 Source Server Version : 100422 (10.4.22-MariaDB)
 Source Host           : localhost:3306
 Source Schema         : users

 Target Server Type    : MySQL
 Target Server Version : 100422 (10.4.22-MariaDB)
 File Encoding         : 65001

 Date: 20/05/2024 14:35:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for book
-- ----------------------------
DROP TABLE IF EXISTS `book`;
CREATE TABLE `book`  (
  `b_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `b_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `b_photo_1` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `b_photo_2` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `b_photo_3` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `b_photo_4` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `b_photo_5` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `b_describe` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `b_newprice` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `b_oldprice` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `b_author` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `b_publish_company` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `b_publish_time` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `b_isbn` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`b_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of book
-- ----------------------------

-- ----------------------------
-- Table structure for category_temp
-- ----------------------------
DROP TABLE IF EXISTS `category_temp`;
CREATE TABLE `category_temp`  (
  `id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `cname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of category_temp
-- ----------------------------

-- ----------------------------
-- Table structure for manage
-- ----------------------------
DROP TABLE IF EXISTS `manage`;
CREATE TABLE `manage`  (
  `m_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `m_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `m_password` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`m_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of manage
-- ----------------------------

-- ----------------------------
-- Table structure for product_temp
-- ----------------------------
DROP TABLE IF EXISTS `product_temp`;
CREATE TABLE `product_temp`  (
  `id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `pname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `old_price` float NOT NULL,
  `new_price` float NOT NULL,
  `images` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `is_hot` int NULL DEFAULT NULL,
  `is_sell` int NULL DEFAULT NULL,
  `pdate` datetime NULL DEFAULT NULL,
  `click_count` int NULL DEFAULT NULL,
  `counts` int NOT NULL,
  `uid` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `pDesc` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `love_user` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `is_pass` int NULL DEFAULT NULL,
  `head_img` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `csid` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of product_temp
-- ----------------------------
INSERT INTO `product_temp` VALUES ('1', 'Apple iPhone XS Max (A2103) 64GB 金色 全网通（移动4G优先版） 双卡双待', 7299, 6999, '/static/img/2.jpg', NULL, NULL, NULL, NULL, 10, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `product_temp` VALUES ('2', 'Apple 2019 MacBook Pro 16【带触控栏】九代六核i7 16G 512G深空灰', 17333, 16999, '/static/product_test/3.jpeg', NULL, NULL, NULL, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products`  (
  `id` int NOT NULL,
  `pname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `images` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `new_price` decimal(10, 2) NOT NULL,
  `old_price` decimal(10, 2) NOT NULL,
  `description` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of products
-- ----------------------------
INSERT INTO `products` VALUES (1, '飘', '/img/book/piao.jpg', 1.00, 9.90, NULL);
INSERT INTO `products` VALUES (2, '白鹿原', '/img/book/bailuyuan.jpg', 15.00, 25.00, NULL);
INSERT INTO `products` VALUES (3, '悲惨世界', '/img/book/beicanshijie.jpg', 20.00, 30.00, NULL);
INSERT INTO `products` VALUES (4, '月亮和六便士', '/img/book/yueliangheliubianshi.jpg', 20.00, 35.00, NULL);
INSERT INTO `products` VALUES (5, '瓦尔登湖', '/img/book/waerdenghu.jpg', 15.00, 20.00, NULL);
INSERT INTO `products` VALUES (6, '三体', '/img/book/santi.jpg', 20.00, 35.00, NULL);
INSERT INTO `products` VALUES (7, '平凡的世界', '/img/book/pingfandeshijie.jpg', 10.00, 20.00, NULL);
INSERT INTO `products` VALUES (8, '老人与海', '/img/book/laorenyuhai.jpg', 10.00, 20.00, NULL);
INSERT INTO `products` VALUES (9, '哈姆雷特', '/img/book/hamuleite.jpg', 15.00, 30.00, NULL);
INSERT INTO `products` VALUES (10, '百年孤独', '/img/book/bainiangudu.jpg', 10.00, 15.00, NULL);
INSERT INTO `products` VALUES (11, '了不起的盖茨比', '/img/book/lbq.jpg', 20.00, 35.00, NULL);
INSERT INTO `products` VALUES (12, '挪威的森林', '/img/book/nwdsl.jpg', 25.00, 35.00, NULL);

-- ----------------------------
-- Table structure for products2
-- ----------------------------
DROP TABLE IF EXISTS `products2`;
CREATE TABLE `products2`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `pname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `images` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `new_price` decimal(10, 2) NOT NULL,
  `old_price` decimal(10, 2) NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of products2
-- ----------------------------
INSERT INTO `products2` VALUES (5, '百年孤独', '/img/book/bainiangudu.jpg', 10.00, 15.00, NULL);
INSERT INTO `products2` VALUES (6, '悲惨世界', '/img/book/悲惨世界.jpg', 20.00, 30.00, NULL);
INSERT INTO `products2` VALUES (8, '活着', NULL, 1.00, 2.00, NULL);
INSERT INTO `products2` VALUES (10, '悲惨世界', '/img/book/beicanshijie.jpg', 20.00, 30.00, NULL);
INSERT INTO `products2` VALUES (11, '重生穿越异世界', NULL, 100.00, 1000.00, NULL);

-- ----------------------------
-- Table structure for shoppingcart
-- ----------------------------
DROP TABLE IF EXISTS `shoppingcart`;
CREATE TABLE `shoppingcart`  (
  `order_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `b_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `u_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `order_num` int NULL DEFAULT NULL,
  `order_status` int NULL DEFAULT NULL,
  PRIMARY KEY (`order_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of shoppingcart
-- ----------------------------

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `phone` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addr` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `is_ok` int NULL DEFAULT NULL,
  `img_url` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `create_time` datetime NULL DEFAULT NULL,
  `identity` int NULL DEFAULT NULL,
  `scores` int NULL DEFAULT NULL,
  `shop_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `upet_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `uphone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `upsw` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `uage` smallint NULL DEFAULT NULL,
  `usex` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `uaddress` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `ujoin_time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`uphone`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('heka', '13360810343', '12345678910', NULL, NULL, NULL, NULL);
INSERT INTO `users` VALUES ('hlizoo', '15816701111', '123456789', NULL, NULL, NULL, NULL);
INSERT INTO `users` VALUES ('123', '15816701123', '123456', NULL, NULL, NULL, NULL);

SET FOREIGN_KEY_CHECKS = 1;
