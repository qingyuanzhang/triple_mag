delimiter $$

CREATE ALGORITHM=UNDEFINED DEFINER=`hump`@`%` SQL SECURITY DEFINER VIEW `V_STOCK_RECOMMENDER_BONUS` AS select `RECOM`.`recommending_id` AS `usr_to`,`TRADE`.`ex_return` AS `ex_return`,`TRADE`.`seller_id` AS `usr_cause` from (`stock_trade_record` `TRADE` join `member_user_recommender` `RECOM` on((`RECOM`.`recommended_id` = `TRADE`.`seller_id`)))$$

delimiter $$

CREATE ALGORITHM=UNDEFINED DEFINER=`hump`@`%` SQL SECURITY DEFINER VIEW `V_USERS_ID` AS select `max`.`id` AS `max_id`,`mid`.`id` AS `mid_id`,`min`.`id` AS `min_id`,`min`.`number` AS `number` from (`member_user_basic` `min` left join (`member_user_mid_mem` `mid` left join `member_user_max_mem` `max` on((`max`.`user_mid_id` = `mid`.`id`))) on((`mid`.`user_id` = `min`.`id`)))$$

delimiter ;

CREATE OR REPLACE
VIEW    `TripleMag`.`V_REC_GEN3`
AS
SELECT  GEN1.recommending_id AS FATHER , GEN2.recommending_id AS SON ,
        GEN3.recommending_id AS GRANDSON ,
        GEN3.recommended_id AS EXGRANDSON
FROM    member_user_recommender             AS GEN1
        INNER JOIN member_user_recommender  AS GEN2
        ON  GEN2.recommending_id = GEN1.recommended_id
        INNER JOIN member_user_recommender  AS GEN3
        ON  GEN3.recommending_id = GEN2.recommended_id ;

CREATE OR REPLACE
VIEW    `TripleMag`.`V_REC_GEN2`
AS
SELECT  GEN1.recommending_id AS FATHER , GEN2.recommending_id AS SON ,
        GEN2.recommendED_id AS GRANDSON
FROM    member_user_recommender             AS GEN1
        INNER JOIN member_user_recommender  AS GEN2
        ON  GEN2.recommending_id = GEN1.recommended_id;

CREATE OR REPLACE
VIEW    V_STOCK_RECOMMENDER_BONUS
AS
SELECT  RECOM.recommending_id AS usr_to , TRADE.ex_return , TRADE.seller_id AS usr_cause
FROM    stock_trade_record                  AS TRADE
        INNER JOIN  member_user_recommender AS RECOM
        ON          recommended_id = TRADE.seller_id;

