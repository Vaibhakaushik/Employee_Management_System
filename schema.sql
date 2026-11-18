CREATE DATABASE IF NOT EXISTS employee_management;
USE employee_management;

CREATE TABLE IF NOT EXISTS employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    department VARCHAR(100) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL CHECK (salary >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional sample record:
-- INSERT INTO employees (name, email, department, salary)
-- VALUES ('Aarav Sharma', 'aarav@example.com', 'Technology', 35000.00);
