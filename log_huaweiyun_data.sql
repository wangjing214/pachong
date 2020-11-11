CREATE TABLE `log_huaweiyun_data` (
`articleid`  bigint(20) UNSIGNED NOT NULL DEFAULT 0 ,
`content`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`catid`  int(11) NULL DEFAULT 25 ,
`id`  int(11) UNSIGNED NOT NULL AUTO_INCREMENT ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_general_ci
AUTO_INCREMENT=12439
ROW_FORMAT=COMPACT
;

