# 🎓 Student Management System with MySQL + Visualizations

This is a **Tkinter-based desktop application** that allows users to manage student records, connect to a MySQL database, and visualize data using **matplotlib** and **seaborn**. It supports CRUD operations, PDF and Excel export, and interactive data charts.

---

## 🚀 Features

- **Add / Edit / Delete Student Records**
- **Search Functionality**
- **Export to Excel**
- **Generate PDF Report**
- **Data Visualizations:**
  - Bar chart: Total fees per course
  - Line chart: Monthly joining trend
  - Pie chart: Student distribution by course

---

## 🧰 Tech Stack

| Component        | Technology                          |
|------------------|-------------------------------------|
| GUI              | `Tkinter`                           |
| Database         | `MySQL`                             |
| Data Analysis    | `Pandas`                            |
| Visualizations   | `Matplotlib`, `Seaborn`             |
| PDF Generation   | `ReportLab`                         |
| Excel Export     | `pandas.to_excel()`                 |

---


# 🛠️ Setup Instructions

## 1.🔧 MySQL Configuration
CREATE DATABASE STUDENT_MANAGEMENT;

USE STUDENT_MANAGEMENT;

CREATE TABLE students_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    course VARCHAR(100),
    fees FLOAT,
    join_date DATE
);

## 2.📦 Install Required Packages
pip install mysql-connector-python pandas matplotlib seaborn reportlab

## 3.▶️ Run the Application
python script.py

# 📊 Sample Visualizations
| Visualization | Description                                  |
| ------------- | -------------------------------------------- |
| Bar Chart     | Shows total fees collected per course        |
| Line Chart    | Displays student joining trend by month      |
| Pie Chart     | Shows distribution of students among courses |

# 📤 Export Options
Excel Export: Save all student records as an .xlsx file.
PDF Report: Auto-generate a PDF containing student details, counts, and fee summaries.

# 💡 Future Enhancements
Date range filter for visualizations

Authentication/login module

Export filtered search results

Admin dashboard with metrics

# CREATED BY
KARTHIK.M


