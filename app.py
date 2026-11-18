from db import get_connection

def add_employee():
    print("\n--- Add Employee ---")
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    department = input("Department: ").strip()
    salary_text = input("Salary: ").strip()

    if not all([name, email, department, salary_text]):
        print("All fields are required.")
        return

    try:
        salary = float(salary_text)
        if salary < 0:
            raise ValueError
    except ValueError:
        print("Salary must be a valid non-negative number.")
        return

    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO employees (name, email, department, salary)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, department, salary))
        conn.commit()
        print(f"Employee added successfully. Employee ID: {cursor.lastrowid}")
    except Exception as error:
        conn.rollback()
        print(f"Could not add employee: {error}")
    finally:
        cursor.close()
        conn.close()


def view_employees():
    print("\n--- Employee Records ---")
    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT employee_id, name, email, department, salary "
            "FROM employees ORDER BY employee_id"
        )
        rows = cursor.fetchall()

        if not rows:
            print("No employee records found.")
            return

        for employee in rows:
            print(
                f"ID: {employee['employee_id']} | "
                f"Name: {employee['name']} | "
                f"Email: {employee['email']} | "
                f"Department: {employee['department']} | "
                f"Salary: {employee['salary']}"
            )
    except Exception as error:
        print(f"Could not retrieve employees: {error}")
    finally:
        cursor.close()
        conn.close()


def search_employee():
    print("\n--- Search Employee ---")
    employee_id = input("Enter employee ID: ").strip()
    if not employee_id.isdigit():
        print("Employee ID must be a number.")
        return

    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT employee_id, name, email, department, salary "
            "FROM employees WHERE employee_id = %s",
            (int(employee_id),)
        )
        employee = cursor.fetchone()
        if employee:
            for key, value in employee.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
        else:
            print("Employee not found.")
    except Exception as error:
        print(f"Search failed: {error}")
    finally:
        cursor.close()
        conn.close()


def update_employee():
    print("\n--- Update Employee ---")
    employee_id = input("Enter employee ID to update: ").strip()
    if not employee_id.isdigit():
        print("Employee ID must be a number.")
        return

    name = input("New name: ").strip()
    email = input("New email: ").strip()
    department = input("New department: ").strip()
    salary_text = input("New salary: ").strip()

    if not all([name, email, department, salary_text]):
        print("All fields are required.")
        return

    try:
        salary = float(salary_text)
        if salary < 0:
            raise ValueError
    except ValueError:
        print("Salary must be a valid non-negative number.")
        return

    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        query = """
            UPDATE employees
            SET name = %s, email = %s, department = %s, salary = %s
            WHERE employee_id = %s
        """
        cursor.execute(query, (name, email, department, salary, int(employee_id)))
        conn.commit()
        if cursor.rowcount:
            print("Employee updated successfully.")
        else:
            print("Employee not found.")
    except Exception as error:
        conn.rollback()
        print(f"Update failed: {error}")
    finally:
        cursor.close()
        conn.close()


def delete_employee():
    print("\n--- Delete Employee ---")
    employee_id = input("Enter employee ID to delete: ").strip()
    if not employee_id.isdigit():
        print("Employee ID must be a number.")
        return

    confirm = input(f"Are you sure you want to delete employee {employee_id}? (y/n): ")
    if confirm.lower() != "y":
        print("Delete cancelled.")
        return

    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM employees WHERE employee_id = %s",
            (int(employee_id),)
        )
        conn.commit()
        if cursor.rowcount:
            print("Employee deleted successfully.")
        else:
            print("Employee not found.")
    except Exception as error:
        conn.rollback()
        print(f"Delete failed: {error}")
    finally:
        cursor.close()
        conn.close()


def main():
    actions = {
        "1": add_employee,
        "2": view_employees,
        "3": search_employee,
        "4": update_employee,
        "5": delete_employee,
    }

    while True:
        print("\n========== EMPLOYEE MANAGEMENT SYSTEM ==========")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Search Employee by ID")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("0. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Thank you for using the Employee Management System.")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option. Please choose 0 to 5.")


if __name__ == "__main__":
    main()
