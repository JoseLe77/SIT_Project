UPDATE
	users
SET
	usr_id = '{}',
	usr_nam = '{}',
	usr_surnam = '{}',
	wh_id = '{}',

	hie_id = (SELECT hie_id  FROM hierarchies h   WHERE hie_nam = '{}'),
	pri_id = (SELECT pri_id  FROM "privileges" p  WHERE pri_nam ='{}'),
	usr_active =  {}
WHERE usr_id = '{}'
	AND wh_id = '{}';