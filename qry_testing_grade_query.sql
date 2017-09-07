SELECT course_dim.canvas_id as course_canvas_id, course_dim.name as course_name, 
enrollment_dim.type as enrollment_type, user_dim.canvas_id as user_canvas_id, user_dim.name as user_name, user_dim.workflow_state as user_workflow_state,
enrollment_fact.computed_final_score as enrollment_fact_computed_final_score, enrollment_fact.computed_current_score as enrollment_fact_computed_current_score,
score_fact.current_score as score_fact_current_score, score_fact.final_score as score_fact_final_score
FROM course_dim
LEFT OUTER JOIN enrollment_dim ON (enrollment_dim.course_id = course_dim.id)
LEFT OUTER JOIN user_dim ON (enrollment_dim.user_id = user_dim.id)
LEFT OUTER JOIN enrollment_fact ON (enrollment_dim.id = enrollment_fact.enrollment_id)
LEFT OUTER JOIN score_fact ON (enrollment_dim.id = score_fact.enrollment_id)
--WHERE course_dim.name = 'Dave Hall Sandbox'
WHERE enrollment_dim.workflow_state <> 'deleted'
AND enrollment_dim.type like '%Student%'
ORDER BY course_canvas_id, user_dim.name;

/*
SELECT enrollment_dim.* 
FROM course_dim, enrollment_dim, user_dim, enrollment_fact 
WHERE enrollment_id.user_id = 86913815536686251 
AND enrollment_dim.user_id = user_dim.id 
AND enrollment_dim.id = enrollment_fact.enrollment_id
AND course_dim.id = enrollment_dim.course_id AND course_dim.canvas_id = 9028
AND enrollment_dim.workflow_state <> 'deleted';
*/
