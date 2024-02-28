SELECT
	hie_nam,
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
		h.hie_num,
		h.hie_nam,
		u2.usr_active,
		COUNT(u2.usr_id) as "User"
	FROM
		users u2 ,
		hierarchies h
	WHERE
		u2.hie_id = h.hie_id
		AND u2.usr_active = 1
		AND u2.wh_id = '{}'
	GROUP BY
		u2.wh_id,
		h.hie_num,
		h.hie_nam,
		u2.usr_active
UNION ALL
	SELECT
		u3.wh_id,
		h2.hie_num,
		h2.hie_nam,
		usr_active,
		COUNT(u3.usr_id) as "User"
	FROM
		users u3 ,
		hierarchies h2
	WHERE
		u3.hie_id = h2.hie_id
		AND u3.usr_active = 0
		AND u3.wh_id = '{}'
	GROUP BY
		u3.wh_id,
		h2.hie_num,
		h2.hie_nam,
		u3.usr_active)
GROUP BY
	hie_nam
ORDER BY hie_nam DESC