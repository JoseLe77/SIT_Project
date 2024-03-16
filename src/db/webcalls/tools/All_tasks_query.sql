SELECT * FROM (SELECT
	t.todo_id,
	t.todo_nam,
	t.todo_description,
	CASE
		WHEN t.todo_comments IS NULL
		OR t.todo_comments = '' THEN 'No comments'
		ELSE t.todo_comments
	END todo_comments,
	t.todo_status,
	s.status,
	t.target_dte
FROM
	todo t,
	statuses s
WHERE
	t.todo_status = s.sts_code
	AND t.todo_status != 'D'
	AND t.wh_id ='{}'
	AND t.usr_id ='{}'
ORDER BY
	t.todo_status DESC)
UNION ALL
SELECT * FROM (SELECT
	t.todo_id,
	t.todo_nam,
	t.todo_description,
	CASE
		WHEN t.todo_comments IS NULL
		OR t.todo_comments = '' THEN 'No comments'
		ELSE t.todo_comments
	END todo_comments,
	t.todo_status,
	s.status,
	t.target_dte
FROM
	todo t,
	statuses s
WHERE
	t.todo_status = s.sts_code
	AND t.todo_status = 'D'
	AND t.wh_id ='{}'
	AND t.usr_id ='{}')