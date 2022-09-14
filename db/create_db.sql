# CREATE TABLE `products` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`name` TEXT NOT NULL,
# 	`active` BOOLEAN NOT NULL DEFAULT FALSE,
# 	`category_id` INT NOT NULL,
# 	`description` TEXT,
# 	`comment` TEXT,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`author_id` INT NOT NULL DEFAULT 1,
# 	`image_path` TEXT,
# 	PRIMARY KEY (`id`)
# );
#
# CREATE TABLE `categories` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`name` TEXT NOT NULL,
# 	`active` BOOLEAN NOT NULL DEFAULT TRUE,
# 	`comment` TEXT,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`author_id` INT NOT NULL DEFAULT 1,
# 	PRIMARY KEY (`id`)
# );
#
# CREATE TABLE `warehouses` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`storage_id` INT NOT NULL,
# 	`product_id` INT NOT NULL,
# 	`amount` FLOAT DEFAULT 0,
# 	`item_measure` TEXT NOT NULL,
# 	`reserve` FLOAT DEFAULT 0,
# 	`active` BOOL DEFAULT FALSE,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`author_id` INT NOT NULL DEFAULT 1,
# 	PRIMARY KEY (`id`)
# );
#
# CREATE TABLE `prices` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`product_id` INT NOT NULL,
# 	`item_measure` TEXT NOT NULL,
# 	`item_price` FLOAT NOT NULL,
#    `active` BOOL DEFAULT FALSE,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`author_id` INT NOT NULL DEFAULT 1,
# 	PRIMARY KEY (`id`)
# );
#
# CREATE TABLE `manufacturers` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`name` TEXT NOT NULL,
# 	`address` TEXT NOT NULL,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`author_id` INT NOT NULL,
# 	PRIMARY KEY (`id`)
# );
#
# CREATE TABLE `productions` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`product_id` INT NOT NULL,
# 	`manufacturer_id` INT NOT NULL,
#     `storage_id` INT NOT NULL,
# 	`amount` FLOAT DEFAULT 0,
# 	`item_measure` TEXT NOT NULL,
# 	`date` DATETIME NOT NULL,
#     `operation` VARCHAR(16) NOT NULL,
# 	`comment` TEXT,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`author_id` INT NOT NULL,
# 	PRIMARY KEY (`id`)
# );
#
#
# CREATE TABLE `pickpoints` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`name` TEXT,
# 	`address` TEXT NOT NULL,
# 	`workhours` TEXT,
# 	`phone` TEXT,
# 	`comment` TEXT,
# 	`link_yandex` TEXT,
# 	`link_point` TEXT,
# 	`map_frame` TEXT,
# 	`active` BOOLEAN NOT NULL DEFAULT FALSE,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`author_id` INT NOT NULL,
# 	PRIMARY KEY (`id`)
# );
#
# CREATE TABLE `orders` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`user_id` INT NOT NULL,
# 	`comment` TEXT NOT NULL,
# 	`order_date` DATETIME NOT NULL,
# 	`status` TEXT NOT NULL,
# 	`delivery_date` DATETIME NOT NULL,
# 	`payment_type` VARCHAR(128),
# 	`pickpoint_id` INT NOT NULL,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`author_id` INT NOT NULL,
# 	PRIMARY KEY (`id`)
# );
#
# CREATE TABLE `order_contents` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`date` DATETIME NOT NULL,
# 	`comment` TEXT NOT NULL,
# 	`order_id` INT NOT NULL,
# 	`product_id` INT NOT NULL,
# 	`manufacturer_id` INT NOT NULL,
# 	`storage_id` INT NOT NULL,
# 	`amount` FLOAT DEFAULT 0,
# 	`price_id` INT NOT NULL,
# 	`status` TEXT NOT NULL,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`author_id` INT NOT NULL,
# 	PRIMARY KEY (`id`)
# );
#
#
# CREATE TABLE `users` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`guid` VARCHAR(255),
# 	`login` VARCHAR(255) NOT NULL,
# 	`password` VARCHAR(255),
# 	`role_id` INT NOT NULL,
# 	`fio` VARCHAR(255) NOT NULL,
# 	`email` VARCHAR(255) NOT NULL,
# 	`phone` VARCHAR(20),
# 	`auth_source` INT NOT NULL,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`active` BOOLEAN NOT NULL,
# 	PRIMARY KEY (`id`)
# );
#
# CREATE TABLE `user_roles` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`title` VARCHAR(255) NOT NULL,
# 	`description` TEXT,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`active` BOOLEAN NOT NULL DEFAULT TRUE,
# 	PRIMARY KEY (`id`)
# );
######
# INSERT INTO user_roles(`title`) VALUES (N'Администратор'),(N'Сыровар'),(N'Покупатель')

CREATE TABLE `storages` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` TEXT,
	`address` TEXT NOT NULL,
	`active` BOOLEAN NOT NULL DEFAULT FALSE,
	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
	`author_id` INT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `cart` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`BUYER` INT NOT NULL,
	`PRODUCT` INT NOT NULL,
	`AMOUNT` int NOT NULL,
	`PRICE` INT NOT NULL,
	`CREATED` DATETIME NOT NULL,
	`UPDATED` DATETIME NOT NULL,
	`ACTIVE` BOOLEAN NOT NULL,
	PRIMARY KEY (`ID`)
);
