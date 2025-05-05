	SELECT
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
	statuses s,
	warehouses w
WHERE
	t.todo_status = s.sts_code
	AND t.wh_id = w.wh_id
	AND  t.todo_id = '{}'
	AND t.wh_id = '{}'