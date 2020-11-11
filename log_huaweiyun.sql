CREATE TABLE `log_huaweiyun` (
`id`  bigint(20) UNSIGNED NOT NULL DEFAULT 0 ,
`title`  varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL ,
`descc`  text CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`author`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`date`  datetime NULL DEFAULT NULL ,
`v`  datetime NULL DEFAULT NULL ,
`catid`  int(11) NULL DEFAULT 25 ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_general_ci
ROW_FORMAT=COMPACT
;

