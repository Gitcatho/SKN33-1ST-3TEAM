-- =====================================================================
--  더미(DUMMY) 데이터 일괄 제거  --  recallcardb
-- ---------------------------------------------------------------------
--  더미 행은 모두 PK 9000 이상이므로 아래 한 묶음으로 깨끗이 제거됩니다.
--  (실제 데이터 PK 1~8999 는 영향을 받지 않습니다.)
--  자식 -> 부모 순서로 삭제하여 외래키 제약을 위반하지 않습니다.
-- =====================================================================

USE recallcardb;

DELETE FROM `news`            WHERE `news_id`        >= 9000;
DELETE FROM `recall`          WHERE `recall_id`      >= 9000;
DELETE FROM `service_center`  WHERE `center_id`      >= 9000;
DELETE FROM `car`             WHERE `car_id`         >= 9000;
DELETE FROM `defect_category` WHERE `defect_id`      >= 9000;
DELETE FROM `region`          WHERE `region_id`      >= 9000;
DELETE FROM `manufacturer`    WHERE `manufacturer_id`>= 9000;

SELECT '[DUMMY] data removed (PK >= 9000)' AS result;