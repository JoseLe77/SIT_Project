SELECT
	tools.tool_num,
	tools.tool_name,
	tools.tool_url,
	CASE
		WHEN tools.tool_active = 1 THEN 'Enabled'
		ELSE 'Disabled'
	END tool_active,
	CASE
		WHEN tools.tool_active = 1 THEN 'Disabled'
		ELSE 'Enabled'
	END tool_active_to_change
FROM
	tools
JOIN warehouses ON
	tools.wh_id = warehouses.wh_id
WHERE tools.tool_num = '{}'
	AND tools.wh_id = '{}'
	AND warehouses.wh_active = 1
ORDER BY
	tools.tool_num