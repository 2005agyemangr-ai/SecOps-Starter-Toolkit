-- Average grade points per student
SELECT
    s.full_name,
    ROUND(AVG(e.grade_points), 2) AS gpa,
    COUNT(e.course_id) AS courses_taken
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.full_name
ORDER BY gpa DESC;
