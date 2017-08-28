DROP VIEW IF EXISTS vw_course_with_sandbox_status CASCADE;

CREATE VIEW vw_course_with_sandbox_status
AS
SELECT id as course_dim_id, canvas_id as course_dim_canvas_id, 
sis_source_id as course_dim_sis_source_id, name as course_dim_name, 
created_at as course_dim_created_at,
CASE WHEN (upper(name) like '%SANDBOX%' OR upper(sis_source_id) like '%SANDBOX%') THEN 'sandbox'::text END as sandbox_status,
CASE WHEN (upper(sis_source_id) like '%SANDBOX%') THEN 'from sis_source_id'::text END as sandbox_sis,
CASE WHEN (upper(name) like '%SANDBOX%') THEN 'inferred from course name only'::text END as sandbox_name,
CASE WHEN (upper(sis_source_id) like 'E%SANDBOX%') THEN trim(left(sis_source_id, 6))::text END as inferred_enumber,
CASE WHEN (upper(sis_source_id) like 'V%SANDBOX%') THEN trim(left(sis_source_id, 6))::text END as inferred_vnumber
FROM course_dim
ORDER BY sis_source_id;

DROP VIEW IF EXISTS vw_undeleted_file_count_by_course;

CREATE VIEW vw_undeleted_file_count_by_course
AS
SELECT t1.course_id as file_course_id, count(distinct(t1.file_id)) as course_undeleted_file_count, sum(t1.size) as course_undeleted_file_size_bytes, max(t2.updated_at) as course_most_recent_undeleted_file_update
FROM file_fact t1
LEFT OUTER JOIN file_dim t2 ON (t1.file_id = t2.id)
WHERE t2.file_state <> 'deleted'
GROUP BY t1.course_id;

DROP VIEW IF EXISTS vw_deleted_file_count_by_course;

CREATE VIEW vw_deleted_file_count_by_course
AS
SELECT t1.course_id as file_course_id, count(distinct(t1.file_id)) as course_deleted_file_count, sum(t1.size) as course_deleted_file_size_bytes, max(t2.updated_at) as course_most_recent_deleted_file_update
FROM file_fact t1
LEFT OUTER JOIN file_dim t2 ON (t1.file_id = t2.id)
WHERE t2.file_state = 'deleted'
GROUP BY t1.course_id;


DROP VIEW IF EXISTS vw_quiz_count_by_course;

CREATE VIEW vw_quiz_count_by_course
AS 
SELECT course_id as quiz_course_id, count(distinct(quiz_id)) as course_quiz_count
FROM quiz_fact
GROUP BY course_id
ORDER BY course_quiz_count desc;

DROP VIEW IF EXISTS vw_sandbox_courses_with_counts CASCADE;

CREATE VIEW vw_sandbox_courses_with_counts
AS
SELECT sandbox_status, COALESCE(sandbox_sis, sandbox_name) as sandbox_status_source, course_dim_sis_source_id, 
inferred_enumber, inferred_vnumber, course_dim_name, 
COALESCE(course_undeleted_file_count, 0) as course_file_count_excludingdeletions,
COALESCE(round(course_undeleted_file_size_bytes/1000000, 2), 0) as course_file_volume_mb_excludingdeletions,
GREATEST(course_most_recent_undeleted_file_update::date, course_most_recent_deleted_file_update::date) as course_most_recent_file_update,
COALESCE(course_deleted_file_count, 0) as course_deleted_file_count,
COALESCE(round(course_deleted_file_size_bytes/1000000, 2), 0) as course_deleted_file_volume_mb,
COALESCE(course_quiz_count, 0) as course_quiz_count
FROM vw_course_with_sandbox_status t1 
LEFT OUTER JOIN vw_undeleted_file_count_by_course t2 ON (t1.course_dim_id = t2.file_course_id)
LEFT OUTER JOIN vw_quiz_count_by_course t3 ON (t1.course_dim_id = t3.quiz_course_id)
LEFT OUTER JOIN vw_deleted_file_count_by_course t4 ON (t1.course_dim_id = t4.file_course_id)
WHERE t1.sandbox_status is not null;

DROP VIEW IF EXISTS vw_sandbox_courses_export CASCADE;

CREATE VIEW vw_sandbox_courses_export
AS
SELECT sandbox_status, sandbox_status_source, course_dim_sis_source_id, inferred_enumber, inferred_vnumber, course_dim_name,
course_file_count_excludingdeletions, course_file_volume_mb_excludingdeletions, 
CASE WHEN ((course_file_volume_mb_excludingdeletions >= 2) AND (course_file_count_excludingdeletions >= 2)) THEN 'flag'::text END as flag_field,
course_most_recent_file_update, course_deleted_file_count, course_deleted_file_volume_mb, course_quiz_count
FROM vw_sandbox_courses_with_counts
ORDER BY course_file_count_excludingdeletions desc;

COPY (SELECT * FROM vw_sandbox_courses_export ORDER BY course_file_count_excludingdeletions desc) TO 'E:/canvas_sandbox_courses_with_filecounts_etc.csv' (FORMAT CSV, DELIMITER ',', HEADER ON, ENCODING 'UTF-8', QUOTE '"');

SELECT * FROM vw_sandbox_courses_export;
