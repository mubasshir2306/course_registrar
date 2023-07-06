DROP DATABASE IF EXISTS railway;
CREATE DATABASE railway;
USE railway;

CREATE TABLE students
(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    unix_id VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE courses
(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    moniker VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    department VARCHAR(255) NOT NULL
);

CREATE TABLE prerequisites
(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    course VARCHAR(10) NOT NULL,
    prereq VARCHAR(10) NOT NULL,
    min_grade INTEGER NOT NULL,
    FOREIGN KEY (course) REFERENCES courses(moniker),
    FOREIGN KEY (prereq) REFERENCES courses(moniker),
    CHECK (min_grade >= 0 AND min_grade <= 100)
);

CREATE TABLE student_course
(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    student VARCHAR(10) NOT NULL,
    course VARCHAR(10) NOT NULL,
    year INTEGER,
    grade INTEGER,
    FOREIGN KEY (student) REFERENCES students(unix_id),
    FOREIGN KEY (course) REFERENCES courses(moniker),
    UNIQUE (student, course, year),
    CHECK (grade >= 0 AND grade <= 100)
);

DROP TRIGGER IF EXISTS before_student_course_insert;
CREATE TRIGGER before_student_course_insert
    BEFORE INSERT
    ON student_course
    FOR EACH ROW
BEGIN
    DROP TEMPORARY TABLE IF EXISTS temp_prereq;
    DROP TEMPORARY TABLE IF EXISTS unmet_prereq;
    CREATE TEMPORARY TABLE IF NOT EXISTS temp_prereq
    (
        prereq VARCHAR(10) REFERENCES courses(moniker),
        min_grade INTEGER
    );

    CREATE TEMPORARY TABLE IF NOT EXISTS unmet_prereq
    (
        prereq VARCHAR(10) REFERENCES courses(moniker)
    );

    INSERT INTO temp_prereq(prereq, min_grade)
    SELECT prereq, min_grade FROM prerequisites as p
    WHERE p.course = NEW.course;

    INSERT INTO unmet_prereq(prereq)
    SELECT prereq FROM temp_prereq AS tp
    WHERE tp.prereq NOT IN (SELECT sc.course FROM student_course as sc WHERE sc.student = NEW.student AND sc.grade > tp.min_grade);

    IF (EXISTS(SELECT 1 FROM unmet_prereq) > 0) THEN
        SET @message = CONCAT('Student ', NEW.student, ' cannot take course ', NEW.course, ' because not all prerequisites are met. ');
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = @message;
    END IF;
END;

CREATE TABLE IF NOT EXISTS letter_grade
(
    grade INTEGER NOT NULL,
    letter VARCHAR(10) NOT NULL,
    CHECK ( grade >= 0 AND grade <= 100 )
);