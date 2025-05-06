SELECT
	wh_id || ' - ' || wh_nam AS warehouse_logged
FROM
	warehouses w
WHERE
	(wh_id || ' - ' || wh_nam) = '{}'
	AND wh_active = 1
UNION ALL
SELECT
	wh_id || ' - ' || wh_nam AS warehouse_logged
FROM
	warehouses w
WHERE
	(wh_id || ' - ' || wh_nam) != '{}'
	AND wh_active = 1
