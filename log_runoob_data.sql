CREATE TABLE `log_runoob_data` (
`id`  int(11) UNSIGNED NOT NULL AUTO_INCREMENT ,
`catid`  int(11) NULL DEFAULT 26 ,
`articleid`  int(11) NULL DEFAULT NULL ,
`content`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL ,
PRIMARY KEY (`id`),
UNIQUE INDEX `articleid` (`articleid`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_general_ci
AUTO_INCREMENT=4684
ROW_FORMAT=COMPACT
;
