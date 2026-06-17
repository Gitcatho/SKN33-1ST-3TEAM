DROP TABLE IF EXISTS `news`;
CREATE TABLE `news` (
	`news_id`	INT	NOT NULL AUTO_INCREMENT	COMMENT '뉴스ID',
	`news_title`	VARCHAR(300)	NOT NULL	COMMENT '뉴스제목',
	`news_link`	VARCHAR(500)	NOT NULL	COMMENT '링크',
	`car_id`	INT	NOT NULL	COMMENT '차량ID',
	PRIMARY KEY (`news_id`)
);

DROP TABLE IF EXISTS `recall`;
CREATE TABLE `recall` (
	`recall_id`	INT	NOT NULL AUTO_INCREMENT	COMMENT '리콜 ID',
	`prod_start`	DATE	NULL	COMMENT '생산시작일',
	`prod_end`	DATE	NULL	COMMENT '생산종료일',
	`recall_date`	DATE	NOT NULL	COMMENT '리콜 개시일',
	`recall_count`	INT	NOT NULL	COMMENT '리콜 대수',
	`recall_reason`	TEXT	NOT NULL	COMMENT '리콜 사유',
	`car_id`	INT	NOT NULL	COMMENT '차량ID',
	`defect_id`	INT	NOT NULL	COMMENT '결함 ID',
	PRIMARY KEY (`recall_id`)
);

DROP TABLE IF EXISTS `faq`;
CREATE TABLE `faq` (
	`faq_id`	INT	NOT NULL AUTO_INCREMENT	COMMENT 'faq ID',
	`question`	TEXT	NOT NULL	COMMENT '질문',
	`answer`	TEXT	NOT NULL	COMMENT '답변',
	PRIMARY KEY (`faq_id`)
);

DROP TABLE IF EXISTS `service_center`;
CREATE TABLE `service_center` (
	`center_id`	INT	NOT NULL AUTO_INCREMENT	COMMENT '서비스 센터ID',
	`center_name`	VARCHAR(100)	NULL	COMMENT '센터명',
	`address`	VARCHAR(200)	NULL	COMMENT '주소',
	`phone`	VARCHAR(20)	NULL	COMMENT '전화번호',
	`latitude`	DECIMAL(10,7)	NULL	COMMENT '위도',
	`longitude`	DECIMAL(10,7)	NULL	COMMENT '경도',
	`region_id`	INT	NOT NULL	COMMENT '지역 ID',
	`manufacturer_id`	INT	NOT NULL	COMMENT '제조사 ID',
	PRIMARY KEY (`center_id`)
);

DROP TABLE IF EXISTS `car`;
CREATE TABLE `car` (
	`car_id`	INT	NOT NULL AUTO_INCREMENT	COMMENT '차량ID',
	`model_name`	VARCHAR(100)	NOT NULL	COMMENT '차명',
	`manufacturer_id`	INT	NOT NULL	COMMENT '제조사 ID',
	PRIMARY KEY (`car_id`)
);

DROP TABLE IF EXISTS `defect_category`;
CREATE TABLE `defect_category` (
	`defect_id`	INT	NOT NULL AUTO_INCREMENT	COMMENT '결함 ID',
	`defect_group`	VARCHAR(50)	NOT NULL	COMMENT '결함 대분류',
	PRIMARY KEY (`defect_id`)
);

DROP TABLE IF EXISTS `manufacturer`;
CREATE TABLE `manufacturer` (
	`manufacturer_id`	INT	NOT NULL AUTO_INCREMENT	COMMENT '제조사 ID',
	`name`	VARCHAR(100)	NOT NULL	COMMENT '제조사명',
	`country`	VARCHAR(50)	NOT NULL	COMMENT '국산/수입',
	PRIMARY KEY (`manufacturer_id`)
);

DROP TABLE IF EXISTS `region`;
CREATE TABLE `region` (
	`region_id`	INT	NOT NULL	COMMENT '지역 ID',
	`city`	VARCHAR(50)	NOT NULL	COMMENT '시도명',
	`district`	VARCHAR(50)	NOT NULL	COMMENT '시군구명',
	PRIMARY KEY (`region_id`)
);

ALTER TABLE `car` ADD CONSTRAINT `FK_manufacturer_TO_car_1` FOREIGN KEY (`manufacturer_id`) REFERENCES `manufacturer` (`manufacturer_id`);
ALTER TABLE `recall` ADD CONSTRAINT `FK_car_TO_recall_1` FOREIGN KEY (`car_id`) REFERENCES `car` (`car_id`);
ALTER TABLE `recall` ADD CONSTRAINT `FK_defect_category_TO_recall_1` FOREIGN KEY (`defect_id`) REFERENCES `defect_category` (`defect_id`);
ALTER TABLE `service_center` ADD CONSTRAINT `FK_region_TO_service_center_1` FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`);
ALTER TABLE `service_center` ADD CONSTRAINT `FK_manufacturer_TO_service_center_1` FOREIGN KEY (`manufacturer_id`) REFERENCES `manufacturer` (`manufacturer_id`);
ALTER TABLE `news` ADD CONSTRAINT `FK_car_TO_news_1` FOREIGN KEY (`car_id`) REFERENCES `car` (`car_id`);

SHOW TABLES;