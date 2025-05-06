SELECT
	p.pri_nam
FROM
	users u,
	"privileges" p
WHERE
	u.pri_id = p.pri_id
	AND u.usr_id = '{}'
	AND u.wh_id = '{}'
UNION ALL
SELECT pri_nam
FROM
(SELECT
	p2.pri_num,
	p2.pri_nam
FROM
	"privileges" p2
WHERE
	p2.pri_id  != (SELECT u2.pri_id FROM users u2  WHERE u2.usr_id = '{}' AND u2.wh_id ='{}')
	AND p2.pri_num >= (SELECT p2.pri_num FROM "privileges" p2 WHERE pri_id = '{}')
ORDER BY p2.pri_num DESC)