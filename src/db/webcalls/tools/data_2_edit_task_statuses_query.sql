SELECT
	sts_code ,
	status
FROM
	statuses s
WHERE
	sts_code = '{}'
UNION ALL 
SELECT
	sts_code ,
	status
FROM
	(
	SELECT
		sts_code ,
		status
	FROM
		statuses s
	WHERE
		sts_code != '{}'
	ORDER BY
		sts_code DESC)