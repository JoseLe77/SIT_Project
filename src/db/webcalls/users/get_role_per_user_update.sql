SELECT p.pri_nam FROM users u, "privileges" p  WHERE u.pri_id = p.pri_id AND u.usr_id = '{}' AND u.wh_id ='{}'
UNION ALL
SELECT p2.pri_nam from "privileges" p2 WHERE p2.pri_id  != (SELECT u2.pri_id FROM users u2  WHERE u2.usr_id = '{}' AND u2.wh_id ='{}')