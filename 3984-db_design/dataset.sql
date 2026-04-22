-- =========================================================
-- Database Design & Normalization Lab - Student Dataset
-- This dataset is intentionally denormalized.
-- =========================================================

PRAGMA foreign_keys = OFF;

-- -------------------------
-- Task 0: student_courses
-- -------------------------
DROP TABLE IF EXISTS student_courses;

CREATE TABLE student_courses (
    student_id INTEGER,
    student_name TEXT,
    student_email TEXT,
    course_id TEXT,
    course_name TEXT,
    instructor_name TEXT,
    instructor_email TEXT
);

INSERT INTO student_courses VALUES
(1, 'Alice Johnson', 'alice@example.edu', 'C101', 'Databases',        'Dr. Smith', 'smith@academy.edu'),
(1, 'Alice Johnson', 'alice@example.edu', 'C104', 'Software Design',  'Dr. Smith', 'smith@academy.edu'),
(2, 'Bob Morales',   'bob@example.edu',   'C101', 'Databases',        'Dr. Smith', 'smith@academy.edu'),
(2, 'Bob Morales',   'bob@example.edu',   'C102', 'Python',           'Ms. Lee',   'lee@academy.edu'),
(3, 'Carla Vega',    'carla@example.edu', 'C102', 'Python',           'Ms. Lee',   'lee@academy.edu'),
(4, 'Diego Ruiz',    'diego@example.edu', 'C103', 'Algorithms',       'Dr. Green', 'green@academy.edu'),
(5, 'Emma Stone',    'emma@example.edu',  'C104', 'Software Design',  'Dr. Smith', 'smith@academy.edu'),
(6, 'Farah Khan',    'farah@example.edu', 'C101', 'Databases',        'Dr. Smith', 'smith@academy.edu');

-- -------------------------
-- Task 1: order_lines_flat
-- -------------------------
DROP TABLE IF EXISTS order_lines_flat;

CREATE TABLE order_lines_flat (
    order_id INTEGER,
    order_date TEXT,
    customer_name TEXT,
    customer_email TEXT,
    product_code TEXT,
    product_name TEXT,
    category_name TEXT,
    unit_price_paid REAL,
    quantity INTEGER
);

INSERT INTO order_lines_flat VALUES
(1001, '2026-04-01', 'Alice Johnson', 'alice@example.com', 'P100', 'Laptop',   'Electronics', 1200.00, 1),
(1001, '2026-04-01', 'Alice Johnson', 'alice@example.com', 'P200', 'Mouse',    'Accessories',   25.00, 2),
(1002, '2026-04-02', 'Bob Morales',   'bob@example.com',   'P100', 'Laptop',   'Electronics', 1200.00, 1),
(1003, '2026-04-03', 'Alice Johnson', 'alice@example.com', 'P300', 'Keyboard', 'Accessories',   80.00, 1),
(1004, '2026-04-03', 'Dana Silva',    'dana@example.com',  'P200', 'Mouse',    'Accessories',   25.00, 1),
(1005, '2026-04-04', 'Evan Torres',   'evan@example.com',  'P400', 'Dock',     'Accessories',  150.00, 1),
(1005, '2026-04-04', 'Evan Torres',   'evan@example.com',  'P200', 'Mouse',    'Accessories',   25.00, 1),
(1006, '2026-04-05', 'Bob Morales',   'bob@example.com',   'P300', 'Keyboard', 'Accessories',   80.00, 2);

-- -------------------------
-- Task 2: employees_departments
-- -------------------------
DROP TABLE IF EXISTS employees_departments;

CREATE TABLE employees_departments (
    employee_id INTEGER,
    employee_name TEXT,
    employee_email TEXT,
    department_id INTEGER,
    department_name TEXT,
    department_location TEXT,
    department_manager_email TEXT
);

INSERT INTO employees_departments VALUES
(1, 'Alice Johnson', 'alice@corp.example', 10, 'Engineering', 'New York', 'cto@corp.example'),
(2, 'Bob Morales',   'bob@corp.example',   10, 'Engineering', 'New York', 'cto@corp.example'),
(3, 'Carla Vega',    'carla@corp.example', 20, 'HR',          'London',   'hr-director@corp.example'),
(4, 'Diego Ruiz',    'diego@corp.example', 20, 'HR',          'London',   'hr-director@corp.example'),
(5, 'Emma Stone',    'emma@corp.example',  30, 'Finance',     'Paris',    'finance-head@corp.example'),
(6, 'Farah Khan',    'farah@corp.example', 10, 'Engineering', 'New York', 'cto@corp.example');

-- -------------------------
-- Task 3: conference_registrations_flat
-- -------------------------
DROP TABLE IF EXISTS conference_registrations_flat;

CREATE TABLE conference_registrations_flat (
    attendee_id INTEGER,
    attendee_name TEXT,
    attendee_email TEXT,
    company_name TEXT,
    session_id TEXT,
    session_title TEXT,
    track_name TEXT,
    room_name TEXT,
    speaker_name TEXT,
    speaker_email TEXT
);

INSERT INTO conference_registrations_flat VALUES
(1, 'Alice Johnson', 'alice@startup.com', 'Blue Rocket', 'S101', 'Data Modeling Basics',   'Data',       'Room A', 'Dr. Smith', 'smith@conf.org'),
(1, 'Alice Johnson', 'alice@startup.com', 'Blue Rocket', 'S201', 'API Design Patterns',    'Backend',    'Room C', 'Ms. Lee',   'lee@conf.org'),
(2, 'Bob Morales',   'bob@north.dev',     'North Dev',   'S101', 'Data Modeling Basics',   'Data',       'Room A', 'Dr. Smith', 'smith@conf.org'),
(3, 'Carla Vega',    'carla@north.dev',   'North Dev',   'S301', 'Observability 101',      'DevOps',     'Room D', 'Mr. Patel', 'patel@conf.org'),
(4, 'Diego Ruiz',    'diego@acme.io',     'Acme IO',     'S201', 'API Design Patterns',    'Backend',    'Room C', 'Ms. Lee',   'lee@conf.org'),
(5, 'Emma Stone',    'emma@blue.ai',      'Blue Rocket', 'S401', 'Prompt Engineering Lab', 'Applied AI', 'Room E', 'Dr. Smith', 'smith@conf.org'),
(2, 'Bob Morales',   'bob@north.dev',     'North Dev',   'S401', 'Prompt Engineering Lab', 'Applied AI', 'Room E', 'Dr. Smith', 'smith@conf.org'),
(6, 'Farah Khan',    'farah@acme.io',     'Acme IO',     'S101', 'Data Modeling Basics',   'Data',       'Room A', 'Dr. Smith', 'smith@conf.org');
