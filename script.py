# Student Management System with MySQL + Visualizations
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import mysql.connector
import os

# MySQL Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '', #you have to give your password here
    'database': 'STUDENT_MANAGEMENT'
}
TABLE_NAME = 'students_details'
COURSE_OPTIONS = ["Python", "Data Science", "Web Dev", "Cloud", "AI/ML"]

# Connect to MySQL
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

def fetch_data():
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Name", "Course", "Fees", "Join Date"])
    return df

def insert_data(name, course, fees, join_date):
    cursor.execute(f"INSERT INTO {TABLE_NAME} (name, course, fees, join_date) VALUES (%s, %s, %s, %s)",
                   (name, course, fees, join_date))
    conn.commit()

def update_data(row_id, name, course, fees, join_date):
    cursor.execute(f"UPDATE {TABLE_NAME} SET name=%s, course=%s, fees=%s, join_date=%s WHERE id=%s",
                   (name, course, fees, join_date, row_id))
    conn.commit()

def delete_data(row_id):
    cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id=%s", (row_id,))
    conn.commit()

# GUI Setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("1100x750")
root.configure(bg="#1e1e1e")
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

editing_id = None

# ================= TAB 1: STUDENT RECORDS =================
tab1 = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(tab1, text="Student Records")

tree = ttk.Treeview(tab1, columns=["ID", "Name", "Course", "Fees", "Join Date"], show='headings')
for col in ["ID", "Name", "Course", "Fees", "Join Date"]:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=10)

# Entry Fields
form = tk.Frame(tab1, bg="#2c2c2c")
form.pack(pady=10)

entry_name = tk.Entry(form, width=30)
entry_course = ttk.Combobox(form, values=COURSE_OPTIONS, width=27, state="readonly")
entry_fees = tk.Entry(form, width=30)
entry_date = tk.Entry(form, width=30)

tk.Label(form, text="Name", fg="white", bg="#2c2c2c").grid(row=0, column=0)
entry_name.grid(row=0, column=1, padx=5)

tk.Label(form, text="Course", fg="white", bg="#2c2c2c").grid(row=1, column=0)
entry_course.grid(row=1, column=1, padx=5)

tk.Label(form, text="Fees", fg="white", bg="#2c2c2c").grid(row=2, column=0)
entry_fees.grid(row=2, column=1, padx=5)

tk.Label(form, text="Join Date (YYYY-MM-DD)", fg="white", bg="#2c2c2c").grid(row=3, column=0)
entry_date.grid(row=3, column=1, padx=5)

# Buttons
btn_frame = tk.Frame(tab1, bg="#2c2c2c")
btn_frame.pack(pady=5)

entry_search = tk.Entry(btn_frame)
entry_search.grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Search", command=lambda: search_student()).grid(row=0, column=1)
tk.Button(btn_frame, text="Add/Update", command=lambda: add_student()).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Edit Selected", command=lambda: load_selected()).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Delete Selected", command=lambda: delete_selected()).grid(row=0, column=4, padx=5)
tk.Button(btn_frame, text="Export Excel", command=lambda: export_excel()).grid(row=0, column=5, padx=5)
tk.Button(btn_frame, text="Generate PDF", command=lambda: generate_pdf()).grid(row=0, column=6, padx=5)
 
# ==== CORE FUNCTIONS ====
def refresh_tree():
    for i in tree.get_children():
        tree.delete(i)
    df = fetch_data()
    for _, row in df.iterrows():
        tree.insert('', 'end', values=list(row))

def add_student():
    global editing_id
    name = entry_name.get()
    course = entry_course.get()
    fees = entry_fees.get()
    join_date = entry_date.get()

    if not name or not course or not fees or not join_date:
        messagebox.showwarning("Input Error", "Please fill all fields")
        return
    try:
        fees = float(fees)
        datetime.strptime(join_date, '%Y-%m-%d')
    except:
        messagebox.showerror("Error", "Invalid fees or date")
        return

    if editing_id:
        update_data(editing_id, name, course, fees, join_date)
        editing_id = None
    else:
        insert_data(name, course, fees, join_date)

    clear_entries()
    refresh_tree()

def load_selected():
    global editing_id
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected)['values']
    editing_id = values[0]
    entry_name.delete(0, tk.END)
    entry_name.insert(0, values[1])
    entry_course.set(values[2])
    entry_fees.delete(0, tk.END)
    entry_fees.insert(0, values[3])
    entry_date.delete(0, tk.END)
    entry_date.insert(0, values[4])

def delete_selected():
    selected = tree.selection()
    for item in selected:
        row_id = tree.item(item)['values'][0]
        delete_data(row_id)
    refresh_tree()

def search_student():
    query = entry_search.get().lower()
    df = fetch_data()
    filtered = df[df['Name'].str.lower().str.contains(query) | df['Course'].str.lower().str.contains(query)]
    for row in tree.get_children():
        tree.delete(row)
    for _, row in filtered.iterrows():
        tree.insert('', 'end', values=list(row))

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_course.set('')
    entry_fees.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    global editing_id
    editing_id = None

def export_excel():
    df = fetch_data()
    file = filedialog.asksaveasfilename(defaultextension=".xlsx")
    if file:
        df.to_excel(file, index=False)

def generate_pdf():
    df = fetch_data()
    filename = "Student_Report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Student Report ({datetime.now().strftime('%Y-%m-%d')})")
    c.drawString(50, 730, f"Total Students: {len(df)}")
    c.drawString(50, 710, f"Total Fees: Rs. {df['Fees'].sum()}")
    y = 690
    for i, row in df.iterrows():
        c.drawString(50, y, f"{row['Name']} - {row['Course']} - Rs.{row['Fees']} - {row['Join Date']}")
        y -= 15
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    messagebox.showinfo("PDF Report", f"PDF saved as {filename}")

# =============== TAB 2: VISUALIZATION =====================
tab2 = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(tab2, text="Visualizations")

viz_frame = tk.Frame(tab2, bg="#1e1e1e")
viz_frame.pack(fill="both", expand=True)

fig, axs = plt.subplots(1, 3, figsize=(15, 4))
canvas_fig = FigureCanvasTkAgg(fig, master=viz_frame)
canvas_fig.get_tk_widget().pack(fill="both", expand=True)

# Plot charts
def plot_charts():
    df = fetch_data()
    df['Join Date'] = pd.to_datetime(df['Join Date'])

    axs[0].clear()
    axs[1].clear()
    axs[2].clear()

    # Bar chart - fees per course
    fees_by_course = df.groupby('Course')['Fees'].sum()
    sns.barplot(x=fees_by_course.index, y=fees_by_course.values, ax=axs[0])
    axs[0].set_title("Total Fees by Course")
    axs[0].set_ylabel("Fees")
    axs[0].tick_params(axis='x', rotation=45)

    # Line chart - joining trend
    monthly = df.groupby(df['Join Date'].dt.to_period('M')).size()
    monthly.index = monthly.index.astype(str)
    monthly.plot(ax=axs[1], marker='o')
    axs[1].set_title("Monthly Join Trend")
    axs[1].set_ylabel("Students")
    axs[1].tick_params(axis='x', rotation=45)

    # Pie chart - students by course
    pie_data = df['Course'].value_counts()
    axs[2].pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
    axs[2].set_title("Student Distribution by Course")

    fig.tight_layout()
    canvas_fig.draw()

plot_charts()
refresh_tree()
root.mainloop()
