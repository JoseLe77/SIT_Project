SELECT
	'BUTTONS' SUMMARY,
	COUNT(CASE tool_active WHEN 1 THEN tool_name END) ENABLED,
	COUNT(CASE tool_active WHEN 0 THEN tool_name END) DISABLED
FROM
	tools
WHERE
	wh_id = '{}'
UNION ALL
	SELECT
	'FORMS' SUMMARY,
	COUNT(CASE form_active WHEN 1 THEN form_id END) ENABLED,
	COUNT(CASE form_active WHEN 0 THEN form_id END) DISABLED
FROM
	forms
WHERE
	wh_id = '{}'
UNION ALL
	SELECT
	'USERS' SUMMARY,
	COUNT(CASE usr_active WHEN 1 THEN usr_id END) ENABLED,
	COUNT(CASE usr_active WHEN 0 THEN usr_id END) DISABLED
FROM
	users
WHERE
	wh_id = '{}'