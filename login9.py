import tkinter as tk
from tkinter import messagebox
import pymysql
def connect_database():
    return pymysql.connect(host="localhost",user="root",password="",database="shadowdb")
def open_dashboard(role):
    dashboard = tk.Toplevel(root)
    dashboard.geometry("400x300")
    if role == "student":
        dashboard.title("Student Dashboard")
        tk.Label(dashboard,text="Welcome to Student Dashboard",font=("Arial", 16)).pack(pady=50)
        tk.Button(dashboard,text="STUDENT DATABASE",command=student_addition,font=("Arial", 16)).pack(pady=15)
    elif role == "staff":
        dashboard.title("Staff Dashboard")
        tk.Label(dashboard,text="Welcome to Staff Dashboard",font=("Arial", 16)).pack(pady=50)
    elif role == "admin":
        dashboard.title("Admin Dashboard")
        tk.Label(dashboard,text="Welcome to ADMIN Dashboard",font=("Arial", 16)).pack(pady=30)
        tk.Button(dashboard,text="STUDENT DATABASE",command=student_management,font=("Arial", 16)).pack(pady=15)
        tk.Button(dashboard,text="password",command=password,font=("Arial", 16)).pack(pady=15)
def login():
    email = txtemail.get()
    password = txtpass.get()
    if email == "" or password == "":
        messagebox.showwarning("Warning","Please enter your email and password")
        return
    try:
        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute("SELECT password, role FROM staff WHERE email = %s",(email,))
        user = cursor.fetchone()
        if user is None:
            cursor.execute("SELECT pasword FROM student_account WHERE email = %s",(email,))
            user = cursor.fetchone()
            if user is None:
                messagebox.showerror("Error","Email not found")
                cursor.close()
                connection.close()
                return
            db_password = str(user[0])
            role = "student"
        else:
            db_password = str(user[0])
            role = user[1]
        if password != db_password:
            messagebox.showerror("Error","Incorrect password")
            cursor.close()
            connection.close()
            return
        messagebox.showinfo("Success",f"Login successful!\nRole: {role}")
        cursor.close()
        connection.close()
        root.withdraw()
        open_dashboard(role)
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error",f"Could not connect to database.\n\n{e}")
def student_management():
    oldmatric = None
    verified = False
    def clear_fields():
        nonlocal verified
        txtmatric.delete(0, tk.END)
        txtemai.delete(0, tk.END)
        txtname.delete(0, tk.END)
        txtage.delete(0, tk.END)
        txtlevel.delete(0, tk.END)
        txtadd.delete(0, tk.END)
        txtdept.delete(0, tk.END)
        verified = False
    def save_student():
        matric = txtmatric.get()
        email = txtemai.get()
        name = txtname.get()
        age = txtage.get()
        level = txtlevel.get()
        admissionyear = txtadd.get()
        dept = txtdept.get()
        if matric == "" or email == "" or name == "" or age == "" or level == "" or admissionyear == "" or dept == "":
            messagebox.showwarning("Error", "Please fill in all fields")
            return
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO student (matric_number,email,name,age,level,admission_year,department) VALUES (%s,%s,%s,%s,%s,%s,%s)",(matric,email,name,age,level,admissionyear,dept))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Student Added Successfully")
        clear_fields()
    def search_student():
        nonlocal oldmatric, verified
        matric = txtmatric.get()
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM student WHERE matric_number=%s",(matric,))
        result = cursor.fetchone()
        if result:
            clear_fields()
            oldmatric = result[0]
            verified = True
            txtmatric.insert(0, result[0])
            txtemai.insert(0, result[1])
            txtname.insert(0, result[2])
            txtage.insert(0, result[3])
            txtlevel.insert(0, result[4])
            txtadd.insert(0, result[5])
            txtdept.insert(0, result[6])
            messagebox.showinfo("Success", "Data Found")
        else:
            verified = False
            messagebox.showerror("Error", "No Record Found")
        cursor.close()
        conn.close()
    def update_student():
        nonlocal oldmatric
        if not verified:
            messagebox.showwarning("Error", "Search for a student first")
            return
        matric = txtmatric.get()
        email = txtemai.get()
        name = txtname.get()
        age = txtage.get()
        level = txtlevel.get()
        admissionyear = txtadd.get()
        dept = txtdept.get()
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE student SET matric_number=%s, email=%s, name=%s, age=%s, level=%s, admission_year=%s, department=%s WHERE matric_number=%s",(matric,email,name,age,level,admissionyear,dept,oldmatric))
        conn.commit()
        cursor.close()
        conn.close()
        oldmatric = matric
        messagebox.showinfo("Success", "Update Successful")
    def delete_student():
        nonlocal oldmatric, verified
        if not verified:
            messagebox.showwarning("Error", "Search for a student first")
            return
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE matric_number=%s",(oldmatric,))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Student Deleted")
        oldmatric = None
        clear_fields()
    dash = tk.Toplevel(root)
    dash.title("Student Management")
    dash.geometry("600x500")
    dash.config(bg="#E9D5FF")
    header = tk.Frame(dash, bg="#6D28D9", height=60)
    header.pack(fill="x")
    tk.Label(header,text="STUDENT MANAGEMENT",font=("Arial", 18, "bold"),fg="white",bg="#6D28D9").pack(pady=15)
    body = tk.Frame(dash, bg="#E9D5FF")
    body.pack(pady=20)
    tk.Label(body, text="Matric Number", bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=0, column=0, padx=10, pady=8, sticky="w")
    txtmatric = tk.Entry(body, font=("Arial", 11), width=30)
    txtmatric.grid(row=0, column=1, padx=10, pady=8)
    tk.Label(body, text="Email", bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=1, column=0, padx=10, pady=8, sticky="w")
    txtemai = tk.Entry(body, font=("Arial", 11), width=30)
    txtemai.grid(row=1, column=1, padx=10, pady=8)
    tk.Label(body, text="Name", bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=2, column=0, padx=10, pady=8, sticky="w")
    txtname = tk.Entry(body, font=("Arial", 11), width=30)
    txtname.grid(row=2, column=1, padx=10, pady=8)
    tk.Label(body, text="Age", bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=3, column=0, padx=10, pady=8, sticky="w")
    txtage = tk.Entry(body, font=("Arial", 11), width=30)
    txtage.grid(row=3, column=1, padx=10, pady=8)
    tk.Label(body, text="Level", bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=4, column=0, padx=10, pady=8, sticky="w")
    txtlevel = tk.Entry(body, font=("Arial", 11), width=30)
    txtlevel.grid(row=4, column=1, padx=10, pady=8)
    tk.Label(body, text="Admission Year", bg="#E9D5FF",
             font=("Arial", 11, "bold")).grid(row=5, column=0, padx=10, pady=8, sticky="w")
    txtadd = tk.Entry(body, font=("Arial", 11), width=30)
    txtadd.grid(row=5, column=1, padx=10, pady=8)
    tk.Label(body, text="Department", bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=6, column=0, padx=10, pady=8, sticky="w")
    txtdept = tk.Entry(body, font=("Arial", 11), width=30)
    txtdept.grid(row=6, column=1, padx=10, pady=8)
    actions = tk.Frame(dash, bg="#E9D5FF")
    actions.pack(pady=20)
    tk.Button(actions, text="SEARCH", width=15,bg="#DBEAFE", fg="#1D4ED8",command=search_student).grid(row=0, column=0, padx=8, pady=8)
    tk.Button(actions, text="ADD", width=15,bg="#D1FAE5", fg="#065F46",command=save_student).grid(row=0, column=1, padx=8, pady=8)
    tk.Button(actions, text="UPDATE", width=15,bg="#FEF3C7", fg="#92400E",command=update_student).grid(row=1, column=0, padx=8, pady=8)
    tk.Button(actions, text="DELETE", width=15,bg="#FECACA", fg="#991B1B",command=delete_student).grid(row=1, column=1, padx=8, pady=8)
    # tk.Button(actions,root.destroy(student_management) ,text="BACK", width=15,bg="#FECACA",fg="#1D4ED8",command= open_dashboard("admin")).grid(row=1,column=3,padx=8,pady=8)
def student_addition():
    oldmatric = None
    verified = False
    def clear_fields():
        nonlocal verified
        txtmatric.delete(0, tk.END)
        txtemai.delete(0, tk.END)
        txtname.delete(0, tk.END)
        txtage.delete(0, tk.END)
        txtlevel.delete(0, tk.END)
        txtadd.delete(0, tk.END)
        txtdept.delete(0, tk.END)
        verified = False
    def save_student():
        matric = txtmatric.get()
        email = txtemai.get()
        name = txtname.get()
        age = txtage.get()
        level = txtlevel.get()
        admissionyear = txtadd.get()
        dept = txtdept.get()
        if matric == "" or email == "" or name == "" or age == "" or level == "" or admissionyear == "" or dept == "":
            messagebox.showwarning("Error", "Please fill in all fields")
            return
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO student (matric_number,email,name,age,level,admission_year,department) VALUES (%s,%s,%s,%s,%s,%s,%s)",(matric,email,name,age,level,admissionyear,dept))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Student Added Successfully")
        clear_fields()
    def update_student():
        nonlocal oldmatric
        if not verified:
            messagebox.showwarning("Error", "Search for a student first")
            return
        matric = txtmatric.get()
        email = txtemai.get()
        name = txtname.get()
        age = txtage.get()
        level = txtlevel.get()
        admissionyear = txtadd.get()
        dept = txtdept.get()
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE student SET matric_number=%s, email=%s, name=%s, age=%s, level=%s, admission_year=%s, department=%s WHERE matric_number=%s",(matric,email,name,age,level,admissionyear,dept,oldmatric))
        conn.commit()
        cursor.close()
        conn.close()
        clear_fields
        messagebox.showinfo("Success", "Update Successful")
    dash = tk.Toplevel(root)
    dash.title("Student Management")
    dash.geometry("600x500")
    dash.config(bg="#E9D5FF")
    header = tk.Frame(dash, bg="#6D28D9", height=60)
    header.pack(fill="x")
    tk.Label(header,text="STUDENT MANAGEMENT",font=("Arial", 18, "bold"),fg="white",bg="#6D28D9").pack(pady=15)
    body = tk.Frame(dash, bg="#E9D5FF")
    body.pack(pady=20)
    tk.Label(body, text="Matric Number", bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=0, column=0, padx=10, pady=8, sticky="w")
    txtmatric = tk.Entry(body, font=("Arial", 11), width=30)
    txtmatric.grid(row=0, column=1, padx=10, pady=8)
    tk.Label(body, text="Email", bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=1, column=0, padx=10, pady=8, sticky="w")
    txtemai = tk.Entry(body, font=("Arial", 11), width=30)
    txtemai.grid(row=1, column=1, padx=10, pady=8)
    tk.Label(body, text="Name", bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=2, column=0, padx=10, pady=8, sticky="w")
    txtname = tk.Entry(body, font=("Arial", 11), width=30)
    txtname.grid(row=2, column=1, padx=10, pady=8)
    tk.Label(body, text="Age", bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=3, column=0, padx=10, pady=8, sticky="w")
    txtage = tk.Entry(body, font=("Arial", 11), width=30)
    txtage.grid(row=3, column=1, padx=10, pady=8)
    tk.Label(body, text="Level", bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=4, column=0, padx=10, pady=8, sticky="w")
    txtlevel = tk.Entry(body, font=("Arial", 11), width=30)
    txtlevel.grid(row=4, column=1, padx=10, pady=8)
    tk.Label(body, text="Admission Year", bg="#E9D5FF",
             font=("Arial", 11, "bold")).grid(row=5, column=0, padx=10, pady=8, sticky="w")
    txtadd = tk.Entry(body, font=("Arial", 11), width=30)
    txtadd.grid(row=5, column=1, padx=10, pady=8)
    tk.Label(body, text="Department", bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=6, column=0, padx=10, pady=8, sticky="w")
    txtdept = tk.Entry(body, font=("Arial", 11), width=30)
    txtdept.grid(row=6, column=1, padx=10, pady=8)
    actions = tk.Frame(dash, bg="#E9D5FF")
    actions.pack(pady=20)
    tk.Button(actions, text="ADD", width=15,bg="#D1FAE5", fg="#065F46",command=save_student).grid(row=0, column=1, padx=8, pady=8)
    tk.Button(actions, text="UPDATE", width=15,bg="#FEF3C7", fg="#92400E",command=update_student).grid(row=1, column=0, padx=8, pady=8)
def password():
    def passl():
        matri = txtmatric.get()
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student WHERE matric_number=%s",(matri,))
        result = cursor.fetchone()
        if result:
            ts.insert(0, result[1])
            messagebox.showinfo("Success", "Data Found")
        else:
            messagebox.showerror("Error", "No Record Found")
            return
        cursor.close()
        conn.close()
    def paas2():
        matri = txtmatric.get()
        email=ts.get()
        pass9 = txtpasss.get()
        try:
         conn = connect_database()
         cursor = conn.cursor()
         cursor.execute("INSERT INTO student_account (matric_number, email, pasword) VALUES (%s, %s, %s)",
         (matri, email, pass9))
         conn = connect_database()
         cursor = conn.cursor()
         cursor.execute("INSERT INTO student_account (matric_number,email, pasword) VALUES (%s, %s, %s)",(matri,email, pass9))
         conn.commit()
         messagebox.showinfo("Success", "Password Added")
        except pymysql.err.IntegrityError:
         messagebox.showerror("Error", "This student already has an account")
        cursor.close()
        conn.close()
    dash = tk.Toplevel(root)
    dash.title("Student Management")
    dash.geometry("600x500")
    dash.config(bg="#E9D5FF")
    tk.Label(dash,text="Matric Number",bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=0, column=0, padx=10, pady=8, sticky="w")
    txtmatric = tk.Entry(dash,font=("Arial", 11),width=30)
    txtmatric.grid(row=0, column=1, padx=10, pady=8)
    tk.Label(dash,text="Email",bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=1, column=0, padx=10, pady=8, sticky="w")
    ts = tk.Entry(dash,font=("Arial", 11),width=30)
    ts.grid(row=1, column=1, padx=10, pady=8)
    tk.Label(dash,text="PASSWORD",bg="#E9D5FF",font=("Arial", 11, "bold")).grid(row=2, column=0, padx=10, pady=8, sticky="w")
    txtpasss = tk.Entry(dash,font=("Arial", 11),width=30)
    txtpasss.grid(row=2, column=1, padx=10, pady=8)
    tk.Button(dash,text="SEARCH",width=15,bg="#DBEAFE",fg="#1D4ED8",command=passl).grid(row=0, column=2, padx=8, pady=8)
    tk.Button(dash,text="Create password",width=15, bg="#D1FAE5",fg="#065F46",command=paas2).grid(row=2, column=2, padx=8, pady=8)
root = tk.Tk()
root.title("Login System")
root.geometry("400x300")
lbl_email = tk.Label(root,text="Email")
lbl_email.pack(pady=(40, 5))
txtemail = tk.Entry(root,width=35)
txtemail.pack()
lbl_pass = tk.Label(root,text="Password")
lbl_pass.pack(pady=(20, 5))
txtpass = tk.Entry(root,width=35, show="*")
txtpass.pack()
btn_login = tk.Button(root,text="LOGIN",command=login)
btn_login.pack(pady=30)
root.mainloop()