SELECT
	users.usr_id,
	users.usr_nam,
	users.usr_surnam,
	users.hie_id,
	hierarchies.hie_nam,
	users.pri_id,
	p.pri_nam,
	CASE
		WHEN users.usr_active = 1 THEN 'Enabled'
		ELSE 'Disabled'
	END usr_active,
	CASE
		WHEN users.usr_active = 1 THEN 'Disabled'
		ELSE 'Enabled'
	END usr_active_to_change
FROM
	users
JOIN warehouses ON
	users.wh_id = warehouses.wh_id
JOIN "privileges" p ON
	users.pri_id = p.pri_id
JOIN hierarchies ON
	users.hie_id = hierarchies.hie_id
WHERE
	warehouses.wh_active = 1
	AND users.usr_id = '{}'
	AND users.wh_id = '{}'