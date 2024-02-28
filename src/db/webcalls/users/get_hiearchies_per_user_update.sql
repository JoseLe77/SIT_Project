SELECT h.hie_nam FROM users u, hierarchies h  WHERE u.hie_id = h.hie_id AND u.usr_id = '{}' AND u.wh_id ='{}'
UNION ALL
SELECT h2.hie_nam from hierarchies h2 WHERE h2.hie_id  != (SELECT u2.hie_id FROM users u2  WHERE u2.usr_id = '{}' AND u2.wh_id ='{}')