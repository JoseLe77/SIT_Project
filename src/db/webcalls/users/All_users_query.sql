SELECT users.usr_id, users.usr_nam, users.usr_surnam, users.hie_id, hierarchies.hie_nam, users.pri_id, p.pri_nam, CASE WHEN users.usr_active = 1 THEN 'Enabled' ELSE 'Disabled' END usr_active
FROM users
JOIN warehouses ON users.wh_id = warehouses.wh_id
JOIN "privileges" p ON users.pri_id = p.pri_id
JOIN hierarchies ON users.hie_id = hierarchies.hie_id
WHERE warehouses.wh_active = 1
AND users.wh_id = '{}'
AND p.pri_num >= (SELECT p2.pri_num FROM "privileges" p2 WHERE pri_id = '{}')