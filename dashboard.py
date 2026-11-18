import streamlit as st
import pandas as pd
import plotly.express as px
import io
from db import get_connection

st.set_page_config(
    page_title="Employee Management System",
    page_icon="📊",
    layout="wide"
)

# ---------------- DATABASE FUNCTIONS ----------------

def execute_query(query, values=()):
    conn = get_connection()

    if conn is None:
        raise RuntimeError("Could not connect to MySQL.")

    cursor = None

    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return cursor.rowcount

    except Exception:
        conn.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        conn.close()


@st.cache_data(ttl=10)
def load_data():
    conn = get_connection()

    if conn is None:
        return pd.DataFrame()

    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT employee_id, name, email,
                   department, salary, created_at
            FROM employees
            ORDER BY employee_id DESC
        """)

        return pd.DataFrame(cursor.fetchall())

    finally:
        if cursor:
            cursor.close()
        conn.close()


def refresh_dashboard():
    st.cache_data.clear()
    st.rerun()


# ---------------- PAGE HEADER ----------------

st.title("Employee Management & Analytics")
st.caption("Manage employee records and analyse business data.")

df = load_data()

if not df.empty:
    df["salary"] = pd.to_numeric(df["salary"])

# ---------------- ADD EMPLOYEE ----------------

st.header("Employee Operations")

with st.expander("➕ Add New Employee"):
    with st.form("add_employee_form"):
        name = st.text_input("Employee Name")
        email = st.text_input("Email Address")
        department = st.text_input("Department")
        salary = st.number_input(
            "Salary (₹)", min_value=0.0, step=1000.0
        )

        submitted = st.form_submit_button("Add Employee")

        if submitted:
            if not all([name.strip(), email.strip(), department.strip()]):
                st.error("Please complete all fields.")

            elif "@" not in email or "." not in email:
                st.error("Please enter a valid email address.")

            else:
                try:
                    execute_query("""
                        INSERT INTO employees
                        (name, email, department, salary)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        name.strip(),
                        email.strip(),
                        department.strip(),
                        salary
                    ))

                    st.success("Employee added successfully!")
                    refresh_dashboard()

                except Exception as error:
                    st.error(f"Could not add employee: {error}")


# ---------------- UPDATE EMPLOYEE ----------------

if not df.empty:

    with st.expander("✏️ Update Employee"):
        employee_ids = df["employee_id"].tolist()

        selected_id = st.selectbox(
            "Select Employee",
            employee_ids,
            format_func=lambda x: (
                f"{x} - {df.loc[df['employee_id'] == x, 'name'].iloc[0]}"
            ),
            key="update_employee"
        )

        selected = df[df["employee_id"] == selected_id].iloc[0]

        with st.form("update_employee_form"):
            new_name = st.text_input("Name", value=selected["name"])
            new_email = st.text_input("Email", value=selected["email"])
            new_department = st.text_input(
                "Department", value=selected["department"]
            )
            new_salary = st.number_input(
                "Salary",
                min_value=0.0,
                value=float(selected["salary"]),
                step=1000.0
            )

            update_button = st.form_submit_button("Save Changes")

            if update_button:
                if not all([
                    new_name.strip(),
                    new_email.strip(),
                    new_department.strip()
                ]):
                    st.error("All fields are required.")

                elif "@" not in new_email or "." not in new_email:
                    st.error("Please enter a valid email.")

                else:
                    try:
                        execute_query("""
                            UPDATE employees
                            SET name=%s, email=%s,
                                department=%s, salary=%s
                            WHERE employee_id=%s
                        """, (
                            new_name.strip(),
                            new_email.strip(),
                            new_department.strip(),
                            new_salary,
                            selected_id
                        ))

                        st.success("Employee updated successfully!")
                        refresh_dashboard()

                    except Exception as error:
                        st.error(f"Update failed: {error}")


# ---------------- DELETE EMPLOYEE ----------------

if not df.empty:

    with st.expander("🗑️ Delete Employee"):
        with st.form("delete_employee_form"):
            delete_id = st.selectbox(
                "Select employee to delete",
                df["employee_id"].tolist(),
                format_func=lambda x: (
                    f"{x} - {df.loc[df['employee_id'] == x, 'name'].iloc[0]}"
                )
            )

            confirm = st.checkbox(
                "I confirm that I want to delete this employee."
            )

            delete_button = st.form_submit_button("Delete Employee")

            if delete_button:
                if confirm:
                    try:
                        execute_query(
                            "DELETE FROM employees WHERE employee_id=%s",
                            (delete_id,)
                        )
                        st.success("Employee deleted successfully!")
                        refresh_dashboard()

                    except Exception as error:
                        st.error(f"Delete failed: {error}")
                else:
                    st.warning("Please confirm before deleting.")


# ---------------- REFRESH DATA ----------------

st.divider()
st.header("Business Analytics")

if df.empty:
    st.info("No employees found. Add your first employee above.")

else:
    # KPI calculations
    total = len(df)
    average = df["salary"].mean()
    highest = df["salary"].max()
    department_count = df["department"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Employees", total)
    col2.metric("Average Salary", f"₹{average:,.2f}")
    col3.metric("Highest Salary", f"₹{highest:,.2f}")
    col4.metric("Departments", department_count)

    st.divider()

    # Department analysis
    left, right = st.columns(2)

    with left:
        dept_data = (
            df.groupby("department")
            .size()
            .reset_index(name="Employees")
        )

        fig = px.bar(
            dept_data,
            x="department",
            y="Employees",
            title="Employees by Department"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        salary_data = (
            df.groupby("department")["salary"]
            .mean()
            .reset_index()
        )

        fig = px.pie(
            dept_data,
            names="department",
            values="Employees",
            title="Department Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    salary_chart = px.bar(
        salary_data,
        x="department",
        y="salary",
        title="Average Salary by Department"
    )

    st.plotly_chart(salary_chart, use_container_width=True)

    # Search and filter
    st.header("Employee Records")

    search = st.text_input("Search employee by name or email")

    department_options = ["All"] + sorted(
        df["department"].dropna().unique().tolist()
    )

    selected_department = st.selectbox(
        "Filter by department",
        department_options
    )

    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered["name"].str.contains(
                search, case=False, na=False
            ) |
            filtered["email"].str.contains(
                search, case=False, na=False
            )
        ]

    if selected_department != "All":
        filtered = filtered[
            filtered["department"] == selected_department
        ]

    st.dataframe(filtered, use_container_width=True)

    # CSV report
    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Employee Report (CSV)",
        data=csv,
        file_name="employee_report.csv",
        mime="text/csv"
    )
    # Excel Report
    

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        filtered.to_excel(
            writer,
            index=False,
            sheet_name="Employees"
        )

    st.download_button(
        label="Download Employee Report (Excel)",
        data=excel_buffer.getvalue(),
        file_name="employee_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )