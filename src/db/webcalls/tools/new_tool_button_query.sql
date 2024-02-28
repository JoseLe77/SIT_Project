INSERT INTO tools
(tool_num, tool_name, tool_url, wh_id, hie_id, tool_active)
VALUES((SELECT MAX(tool_num)+1 tool_num FROM tools WHERE wh_id = '{}'),'{}','{}','{}', NULL ,0)

