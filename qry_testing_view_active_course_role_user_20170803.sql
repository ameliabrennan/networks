--Sarah August 3 2017
--Prototype SQL for selecting user/course sessions for teachers and then exporting time on task
--Based on discussion with Pablo and Brooke
--This SQL should form the prototype of standard queries to be used in the future
--It selects course codes and non-student users, then uses the requests table to summarise time-on-task and request-count by user, course, and day
--Working well except for active days with only one request: this will appear as no time on task, when a truly inactive day will be null

--PART 1: list of course/role/user combinations, excluding enrollment type student
--If needed, place restrictions here on course types before proceeding (to minimise size of next query)
DROP VIEW IF EXISTS vw_course_role_user CASCADE;

CREATE VIEW vw_course_role_user AS
SELECT course_dim.code as course_code, course_dim.id as course_id, course_dim.sis_source_id as course_term, enrollment_dim.type as user_course_role, user_dim.sortable_name as user_name, enrollment_dim.user_id, enrollment_dim.workflow_state as enrollment_workflow_state
FROM enrollment_dim, course_dim, user_dim
WHERE enrollment_dim.course_id = course_dim.id
AND enrollment_dim.user_id = user_dim.id
--AND (course_dim.sis_source_id like '%1745%' OR course_dim.sis_source_id like '%1750%')
AND (enrollment_dim.type not like '%Student%')
AND (enrollment_dim.workflow_state <> 'deleted')
--TEST RESTRICTIONS
--AND (course_dim.code IN ('BIOL2273', 'AERO2307'))
ORDER BY course_dim.code, course_dim.id, course_dim.sis_source_id, enrollment_dim.type, user_dim.sortable_name, enrollment_dim.user_id, enrollment_dim.workflow_state;

--PART 2: join the list of course/role/user to the requests table (matcihng course_id and user_id), pick up session_id's and timestamps to form a log of activity
--This query will take a long time as the requests table is very large
DROP VIEW IF EXISTS vw_user_course_session_log CASCADE;

CREATE VIEW vw_user_course_session_log AS
SELECT course_code, vw_course_role_user.course_id, course_term, user_course_role, user_name, vw_course_role_user.user_id, enrollment_workflow_state,
requests.timestamp_day, requests.id as request_id, requests.session_id, requests.timestamp_utc
FROM vw_course_role_user
LEFT OUTER JOIN requests
ON ((vw_course_role_user.user_id = requests.user_id) AND (vw_course_role_user.course_id = requests.course_id))
ORDER BY course_code, vw_course_role_user.course_id, course_term, user_course_role, user_name, vw_course_role_user.user_id, enrollment_workflow_state, requests.session_id, requests.timestamp_utc;

--PART 3: summarise the log of activity by day

DROP VIEW IF EXISTS vw_user_course_times_byday CASCADE;

CREATE VIEW vw_user_course_times_byday AS 
SELECT course_code, course_id, course_term, user_course_role, user_name, user_id, enrollment_workflow_state,
timestamp_day, count(distinct(session_id)) as count_canvas_sessions_thisday, 
min(timestamp_utc) as first_request_time_thisday, max(timestamp_utc) as last_request_time_thisday,
count(distinct(request_id)) as count_requests_thisday
FROM vw_user_course_session_log
GROUP BY course_code, course_id, course_term, user_course_role, user_name, user_id, enrollment_workflow_state, timestamp_day
ORDER BY course_code, course_id, course_term, user_course_role, user_name, user_id, enrollment_workflow_state, timestamp_day;

--PART 4: further formatting the summary of activity by day, and add a calculation of minutes on task
--Note that single-requests will return a problematic result here, 0 minutes
--A truly inactive day will have 0 requests
DROP VIEW IF EXISTS vw_user_course_timeontask_byday CASCADE;

CREATE VIEW vw_user_course_timeontask_byday AS
SELECT course_code::text, course_id::text, course_term, user_course_role, user_name, user_id::text, enrollment_workflow_state, timestamp_day, count_canvas_sessions_thisday, 
first_request_time_thisday, last_request_time_thisday,
count_requests_thisday,
((EXTRACT(HOUR FROM (last_request_time_thisday - first_request_time_thisday)) * 3600) + (EXTRACT(MINUTE FROM (last_request_time_thisday - first_request_time_thisday)) * 60)
+ EXTRACT(SECOND FROM (last_request_time_thisday - first_request_time_thisday)))/60 as timeontask_today_minutes
FROM vw_user_course_times_byday
ORDER BY course_code, course_id, course_term, user_course_role, user_name, user_id, enrollment_workflow_state, timestamp_day;

--EXPORT RESULTS TO CSV FILE

COPY (SELECT * FROM vw_user_course_timeontask_byday) TO 'E:/canvas_user_course_timeontask_test_20170803.csv' (FORMAT CSV, DELIMITER ',', ENCODING 'UTF8', HEADER TRUE, QUOTE '"');