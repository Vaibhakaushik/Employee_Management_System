# Employee_Management_System
Developed a Python-based Employee Management System using Streamlit and MySQL, featuring CRUD operations, employee data management, interactive dashboards, salary and department analytics, search and filtering, and CSV/Excel report generation using Pandas and Plotly.

# Employee Management & Analytics Dashboard

## About the Project
The Employee Management & Analytics Dashboard is a Python-based web application developed using Streamlit and MySQL. It helps manage employee records and provides useful insights through interactive dashboards.

The application allows users to add, update, delete, search, and filter employee records. It also displays employee statistics and generates reports in CSV and Excel formats.

## Features
- Add new employee records
- Update existing employee information
- Delete employee records with confirmation
- View total employees and salary statistics
- Analyze department-wise employee distribution
- Visualize average salary by department
- Search employees by name or email
- Filter employees by department
- Export employee data to CSV and Excel

## Technologies Used
- Python
- Streamlit
- MySQL
- Pandas
- Plotly
- OpenPyXL

## Project Structure

```text
Employee_Management_System/
│
├── dashboard.py
├── db.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Employee_Management_System.git
```

### 2. Navigate to the Project Folder

```bash
cd Employee_Management_System
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL
- Create a MySQL database.
- Create the required `employees` table.
- Configure your database connection settings in `db.py`.

### 5. Run the Application

```bash
streamlit run dashboard.py
```

## Dashboard Insights
The dashboard provides:
- Total employee count
- Average employee salary
- Highest employee salary
- Number of departments
- Department-wise employee distribution
- Average salary by department

## Future Improvements
- Add user authentication
- Implement role-based access
- Add employee attendance management
- Improve dashboard reporting

## Author
Vaibhav Kaushik

GitHub: https://github.com/your-username
