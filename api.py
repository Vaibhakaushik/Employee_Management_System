from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from db import get_connection

app = FastAPI(
    title="Employee Management API",
    description="REST API for Employee Management System",
    version="1.0"
)


# Employee data validation
class Employee(BaseModel):
    name: str
    email: EmailStr
    department: str
    salary: float


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    salary: Optional[float] = None


# Test API
@app.get("/")
def home():
    return {"message": "Employee Management API is running!"}


# GET: View all employees
@app.get("/employees")
def get_employees():
    conn = get_connection()

    if not conn:
        raise HTTPException(500, "Database connection failed")

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM employees")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


# GET: Search employee by ID
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    conn = get_connection()

    if not conn:
        raise HTTPException(500, "Database connection failed")

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM employees WHERE employee_id = %s",
            (employee_id,)
        )

        employee = cursor.fetchone()

        if not employee:
            raise HTTPException(404, "Employee not found")

        return employee
    finally:
        cursor.close()
        conn.close()


# POST: Add employee
@app.post("/employees")
def add_employee(employee: Employee):
    conn = get_connection()

    if not conn:
        raise HTTPException(500, "Database connection failed")

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """INSERT INTO employees
            (name, email, department, salary)
            VALUES (%s, %s, %s, %s)""",
            (
                employee.name,
                employee.email,
                employee.department,
                employee.salary
            )
        )

        employee_id = cursor.lastrowid
        conn.commit()

        return {
            "message": "Employee added successfully",
            "employee_id": employee_id
        }
    finally:
        cursor.close()
        conn.close()


# PUT: Update employee
@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeUpdate):
    updates = employee.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(400, "No update data provided")

    conn = get_connection()

    if not conn:
        raise HTTPException(500, "Database connection failed")

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT employee_id FROM employees WHERE employee_id = %s",
            (employee_id,)
        )

        if not cursor.fetchone():
            raise HTTPException(404, "Employee not found")

        allowed_columns = {"name", "email", "department", "salary"}

        for column in updates:
            if column not in allowed_columns:
                raise HTTPException(400, "Invalid field")

        set_clause = ", ".join(
            f"{column} = %s" for column in updates
        )

        values = list(updates.values()) + [employee_id]

        cursor.execute(
            f"UPDATE employees SET {set_clause} WHERE employee_id = %s",
            values
        )

        conn.commit()

        return {"message": "Employee updated successfully"}
    finally:
        cursor.close()
        conn.close()


# DELETE: Remove employee
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    conn = get_connection()

    if not conn:
        raise HTTPException(500, "Database connection failed")

    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM employees WHERE employee_id = %s",
            (employee_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(404, "Employee not found")

        conn.commit()

        return {"message": "Employee deleted successfully"}
    finally:
        cursor.close()
        conn.close()