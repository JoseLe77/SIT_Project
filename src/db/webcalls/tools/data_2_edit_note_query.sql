SELECT
	Notes.note_id,
	Notes.note_title,
	Notes.note_description
FROM
	Notes
JOIN warehouses
ON Notes.wh_id = warehouses.wh_id
WHERE Notes.note_id = '{}'
AND Notes.usr_id = '{}'
and Notes.wh_id = '{}'
AND warehouses.wh_active = 1
AND Notes.note_active = 1