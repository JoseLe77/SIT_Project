SELECT
	wh_num,
	wh_id,
	wh_nam,
	CASE
		WHEN wh_active = 1 THEN 1
		ELSE 0
	END wh_active1_value,
	CASE
		WHEN wh_active = 1 THEN 'Enabled'
		ELSE 'Disabled'
	END wh_active1,
	CASE
		WHEN wh_active = 1 THEN 0
		ELSE 1
	END wh_active2_value,
	CASE
		WHEN wh_active = 0 THEN 'Enabled'
		ELSE 'Disabled'
	END wh_active2
FROM
	warehouses w
WHERE
	wh_num = {}