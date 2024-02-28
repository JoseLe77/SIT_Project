SELECT
	COUNT(f.form_nam) FORMS,
	COUNT(CASE WHEN f.form_active = 1 THEN f.form_nam END) ENABLED_FORMS,
	COUNT(CASE WHEN f.form_active = 0 THEN f.form_nam END) DISABLED_FORMS
FROM
	forms f
WHERE
	wh_id = '{}'