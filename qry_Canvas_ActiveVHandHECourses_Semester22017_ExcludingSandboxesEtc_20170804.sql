--Canvas query developed by Peter August 4th 2017
--List of Active VE and HE Canvas courses, Semester 2, 2017
--Returns a summary of course information and the counts of active student enrollments and active teacher enrollments for each course
--Weeds out sandboxes and only includes these particular semesters (1745 and 1750, Semester 2 on shore) 
--The course code 'C3310' (Certificate II in ELA0 is specifically excluded because it is "more like a program than a course"
--There are five courses WITHIN this course, therefore it is not behaving like a course in the true senseand is more like a program, excluded for this summary script

SELECT * 
FROM 
	(SELECT qc.course_id AS course_id, qc.course_code AS course_code, qc.sis_source_id, qc.course_start, qc.course_end, qstd.student_count, qteacher.teacher_count
	FROM 
		(	
		SELECT cd.id AS course_id, cd.code AS course_code,  cd.sis_source_id AS sis_source_id, etd.date_start AS course_start, etd.date_end AS course_end
		FROM course_dim cd, enrollment_term_dim etd 
		WHERE cd.enrollment_term_id = etd.id 
		AND cd.workflow_state = 'available'
		AND cd.sis_source_id NOT LIKE '%Sandbox%' 
		AND cd.code NOT LIKE '%C3310%' 
		AND (cd.sis_source_id LIKE '%1745%'  OR cd.sis_source_id LIKE '%1750%')
		) qc
		LEFT OUTER JOIN 
			(	
			SELECT course_id, count(*) AS student_count 
			FROM enrollment_dim 
			WHERE type in ('StudentEnrollment')
			AND workflow_state = 'active'
			GROUP BY course_id 
			ORDER BY course_id
			) qstd          
			ON (qc.course_id = qstd.course_id)
			LEFT OUTER JOIN 
				(
				SELECT course_id, count(*) AS teacher_count
				FROM enrollment_dim
				WHERE (type in ('TeacherEnrollment') 
				AND workflow_state = 'active')
				GROUP BY course_id
				ORDER BY course_id
				) qteacher 
				ON (qc.course_id = qteacher.course_id)
	ORDER BY qc.course_code
	) qst
WHERE qst.student_count > 0; 
