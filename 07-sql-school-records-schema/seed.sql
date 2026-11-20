INSERT OR IGNORE INTO students (full_name, email, level, enrolled_date) VALUES
    ('Kwame Mensah', 'kwame.mensah@example.edu', 200, '2025-10-01'),
    ('Ama Boateng', 'ama.boateng@example.edu', 200, '2025-10-01'),
    ('Kofi Owusu', 'kofi.owusu@example.edu', 100, '2026-10-01');

INSERT OR IGNORE INTO courses (course_code, title, credits) VALUES
    ('INF 213', 'Web Technology I', 3),
    ('INF 215', 'Database Management Systems', 3),
    ('CSC 201', 'Computer Architecture', 3);

INSERT OR IGNORE INTO enrollments (student_id, course_id, grade_points) VALUES
    (1, 1, 3.8),
    (1, 2, 3.5),
    (2, 1, 4.0),
    (2, 3, 3.7),
    (3, 1, 3.2);
