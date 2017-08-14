--Query for Pablo August 14th 2017, list of users and their roles for a specific list of courses, up to July 21st

DROP VIEW IF EXISTS vw_custom_course_role_user_list CASCADE;

CREATE VIEW vw_custom_course_role_user_list AS
SELECT course_dim.code as course_code, user_dim.sortable_name as user_name, enrollment_dim.type as user_course_role,  enrollment_dim.user_id::text, course_dim.sis_source_id as course_term, 
enrollment_dim.workflow_state as enrollment_workflow_state, 
enrollment_dim.created_at::date
FROM enrollment_dim, course_dim, user_dim
WHERE enrollment_dim.course_id = course_dim.id
AND enrollment_dim.created_at::date <= '2017-07-21'
AND enrollment_dim.user_id = user_dim.id
AND (enrollment_dim.type not like '%Student%')
AND course_dim.code in ('MEDS2143', 'BIOL2273', 'ONPS2153', 'GEOM2069', 'COSC2669', 'MATH1293', 'BIOL2417', 'BIOL2416', 'EEET1089', 'EEET1152', 'MIET2125', 'COTH2138', 'COTH2188')
AND (enrollment_dim.workflow_state <> 'deleted')
ORDER BY course_dim.code, user_dim.sortable_name, enrollment_dim.type, course_dim.sis_source_id, enrollment_dim.user_id, enrollment_dim.workflow_state;

SELECT * FROM vw_custom_course_role_user_list;
