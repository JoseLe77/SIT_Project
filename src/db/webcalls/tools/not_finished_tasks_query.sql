SELECT
	todo_id,
	todo_nam,
	todo_description,
	todo_comments,
	todo_status,
	status,
	target_dte,
	date_order
FROM
	(
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
		strftime('%d-%m-%Y', t.target_dte) target_dte,
			strftime('%Y%m', target_dte) date_order
	FROM
		todo t,
		statuses s
	WHERE
		t.todo_status = s.sts_code
		AND t.todo_status != 'D'
		AND t.wh_id ='{}'
		AND t.usr_id ='{}')
ORDER BY date_order,target_dte