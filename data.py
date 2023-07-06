students = [
    ('John', 'Doe', 'jd1'),
    ('Jane', 'Doe', 'jd2'),
    ('Andy', 'Bek', 'ab1'),
    ('Sonya', 'Barzel', 'sb1')
]

courses = [
    ('CS101', 'Introduction to Computer Science', 'Computer Science'),
    ('CS304', 'Data Structures', 'Computer Science'),
    ('ECON101', 'Introduction to Economics', 'Economics'),
    ('ECON255', 'Econometrics', 'Economics'),
    ('MATH102', 'Statistical Methods', 'Mathematics'),
    ('MATH201', 'Linear Algebra', 'Mathematics'),
    ('MATH209', 'Discrete Mathematics', 'Mathematics'),
    ('CS301', 'Design and Analysis of Algorithm', 'Computer Science'),
    ('PE215', 'Operations Research', 'Production'),
    ('PE312', 'Logistics & Supply Chain Management', 'Production')
]

prerequisites = [
    ('ECON255', 'ECON101', 50),
    ('CS304', 'CS101', 60),
    ('CS304', 'MATH209', 50),
    ('MATH209', 'MATH102', 50),
    ('PE312', 'PE215', 60),
    ('CS301', 'CS101', 60),
    ('CS301', 'MATH209', 60),
    ('CS301', 'MATH201', 60)
]

letter_grades = [
    (90, 'A'),
    (80, 'B'),
    (70, 'C'),
    (60, 'D'),
    (0, 'F')
]