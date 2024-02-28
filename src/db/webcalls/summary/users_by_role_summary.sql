SELECT
	pri_nam role,
	SUM(CASE
		WHEN usr_active = 1 THEN user
		ELSE 0
	END) Enabled_Users,
	SUM(CASE
		WHEN usr_active = 0 THEN user
		ELSE 0
	END) Disabled_Users
FROM
	(
	SELECT
		u2.wh_id,
		p.pri_num,
		p.pri_nam,
		u2.usr_active,
		COUNT(u2.usr_id) as "User"
	FROM
		users u2 ,
		"privileges" p
	WHERE
		u2.pri_id = p.pri_id
		AND u2.usr_active = 1
		AND u2.wh_id = '{}'
	GROUP BY
		u2.wh_id,
		p.pri_id,
		p.pri_nam,
		u2.usr_active
UNION ALL
	SELECT
		u3.wh_id,
		p.pri_num ,
		p.pri_nam,
		usr_active,
		COUNT(u3.usr_id) as "User"
	FROM
		users u3 ,
		"privileges" p
	WHERE
		u3.pri_id = p.pri_id
		AND u3.usr_active = 0
		AND u3.wh_id = '{}'
	GROUP BY
		u3.wh_id,
		p.pri_num,
		p.pri_nam,
		u3.usr_active)
GROUP BY
	pri_nam
ORDER BY pri_num DESC