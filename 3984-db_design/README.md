# Database Design & Normalization Lab — Student Package

This package contains the dataset used in the **SQL: Database Design & Normalization** project.

## Files

- `dataset.db` — SQLite database file with all tables needed for the project
- `dataset.sql` — SQL script used to create and populate `dataset.db`

## Tables included

### 1. `student_courses`
Used in **Task 0**.

Why this table is intentionally problematic:
- the same student information appears in multiple rows
- the same course information appears in multiple rows
- the same instructor information appears in multiple rows

Typical anomalies you can observe:
- **update anomaly**: changing an instructor requires multiple updates
- **insert anomaly**: adding a new course without a student does not fit naturally
- **delete anomaly**: deleting the last enrollment for a course removes course information

### 2. `order_lines_flat`
Used in **Task 1**.

Why this table is intentionally problematic:
- customer data is repeated in every order line
- product data is repeated across many orders
- order-level and line-level data are mixed together

### 3. `employees_departments`
Used in **Task 2**.

Why this table is intentionally problematic:
- department data is repeated for every employee in the department
- department attributes depend on `department_id`, not on `employee_id`

### 4. `conference_registrations_flat`
Used in **Task 3**.

Why this table is intentionally problematic:
- attendee data repeats across multiple sessions
- session data repeats across multiple attendees
- speaker, room, and track data are repeated

## How to use the dataset

You can open the database directly with SQLite-compatible tools, or recreate it from the SQL script.

### Recreate the database from the SQL script
```bash
sqlite3 dataset.db < dataset.sql
```

### Example exploration queries
```sql
SELECT * FROM student_courses;
SELECT * FROM order_lines_flat;
SELECT * FROM employees_departments;
SELECT * FROM conference_registrations_flat;
```

## Important note

The tables in this package are **not models to imitate**. They are intentionally denormalized so that you can:
- observe data anomalies,
- understand why poor designs create future maintenance problems,
- redesign them into cleaner schemas.
