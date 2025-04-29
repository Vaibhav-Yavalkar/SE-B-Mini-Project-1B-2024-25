# # #db.py
# # import mysql.connector
# # from mysql.connector import connect, Error
# # from tkinter import messagebox
# #
# # DB_PASSWORD = 'root@1234567890'
# #
# # # Database Connection
# # def connect_to_db():
# #     """
# #     Establish a connection to the MySQL database.
# #     """
# #     try:
# #         return connect(
# #             host="localhost",
# #             user="root",
# #             password=DB_PASSWORD,
# #             database="crm"
# #         )
# #     except mysql.connector.Error as err:
# #         messagebox.showerror("Database Error", f"Error: {err}")
# #         return None
# #
# # # Fetch Data for Analysis
# # def fetch_data(field):
# #     """Fetch data from the database based on the selected field."""
# #     conn = mysql.connector.connect(host="localhost", user="root", password=DB_PASSWORD, database="crm")
# #     cursor = conn.cursor()
# #     query = f"SELECT {field} FROM employee"
# #     cursor.execute(query)
# #     data = [row[0] for row in cursor.fetchall()]
# #     conn.close()
# #     return data
# #
# # # User Registration and Login
# # def save_registration_data(name, email, username, password):
# #     conn = connect_to_db()
# #     if conn:
# #         try:
# #             cursor = conn.cursor()
# #             sql = "INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)"
# #             cursor.execute(sql, (name, email, username, password))
# #             conn.commit()
# #             messagebox.showinfo("Success", "Registration data saved successfully!")
# #         except mysql.connector.Error as err:
# #             messagebox.showerror("Database Error", f"Error: {err}")
# #         finally:
# #             conn.close()
# #
# # def validate_login(username, password):
# #     conn = connect_to_db()
# #     if conn:
# #         try:
# #             cursor = conn.cursor()
# #             sql = "SELECT * FROM users WHERE username = %s AND password = %s"
# #             cursor.execute(sql, (username, password))
# #             return cursor.fetchone()
# #         except Error as err:
# #             messagebox.showerror("Database Error", f"Error: {err}")
# #             return None
# #         finally:
# #             conn.close()
# #
# # # Company CRUD Operations
# # def insert_company_data(company_id, company_name, contact_no, primary_business, secondary_business, since, email, website):
# #     conn = connect_to_db()
# #     cursor = conn.cursor()
# #     sql = """INSERT INTO company (company_id, company_name, contact_no, primary_business, secondary_business, since, email, website)
# #              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
# #     values = (company_id, company_name, contact_no, primary_business, secondary_business, since, email, website)
# #
# #     try:
# #         cursor.execute(sql, values)
# #         conn.commit()
# #         return True
# #     except mysql.connector.Error as err:
# #         print(f"Error: {err}")
# #         return False
# #     finally:
# #         cursor.close()
# #         conn.close()
# #
# # def fetch_companies():
# #     connection = connect_to_db()
# #     cursor = connection.cursor(dictionary=True)
# #     cursor.execute("SELECT company_id, company_name, contact_no, primary_business, secondary_business, since, email, website FROM company")
# #     companies = cursor.fetchall()
# #     cursor.close()
# #     connection.close()
# #     return companies
# #
# # def delete_company(company_id):
# #     conn = connect_to_db()
# #     cursor = conn.cursor()
# #     sql = "DELETE FROM company WHERE company_id = %s"
# #
# #     try:
# #         cursor.execute(sql, (company_id,))
# #         conn.commit()
# #         return True
# #     except mysql.connector.Error as err:
# #         print(f"Error: {err}")
# #         return False
# #     finally:
# #         cursor.close()
# #         conn.close()
# #
# # def update_company(company_id, company_name, contact_no, primary_business, secondary_business, since, email, website):
# #     connection = connect_to_db()
# #     cursor = connection.cursor()
# #
# #     sql = """
# #         UPDATE company SET company_name=%s, contact_no=%s, primary_business=%s, secondary_business=%s, since=%s, email=%s, website=%s WHERE company_id=%s
# #     """
# #     values = (company_name, contact_no, primary_business, secondary_business, since, email, website, company_id)
# #
# #     try:
# #         cursor.execute(sql, values)
# #         connection.commit()
# #         return cursor.rowcount > 0  # Return True if update was successful
# #     except Exception as e:
# #         print("Error updating company:", e)
# #         return False
# #     finally:
# #         cursor.close()
# #         connection.close()
# #
# # # Employee CRUD Operations
# # def fetch_employees():
# #     conn = mysql.connector.connect(host="localhost", user="root", password=DB_PASSWORD, database="crm")
# #     cursor = conn.cursor(dictionary=True)
# #     cursor.execute("SELECT * FROM employee")
# #     employees = cursor.fetchall()
# #     conn.close()
# #     return employees
# #
# # def insert_employee(id, name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company):
# #     conn = mysql.connector.connect(host="localhost", user="root", password=DB_PASSWORD, database="crm")
# #     cursor = conn.cursor()
# #     query = "INSERT INTO employee (id, name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
# #     values = (id, name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company)
# #     cursor.execute(query, values)
# #     conn.commit()
# #     conn.close()
# #     return True
# #
# # def delete_employee(id):
# #     conn = mysql.connector.connect(host="localhost", user="root", password=DB_PASSWORD, database="crm")
# #     cursor = conn.cursor()
# #     query = "DELETE FROM employee WHERE id = %s"
# #     cursor.execute(query, (id,))
# #     conn.commit()
# #     conn.close()
# #     return True
# #
# # def update_employee(id, name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company):
# #     conn = mysql.connector.connect(host="localhost", user="root", password=DB_PASSWORD, database="crm")
# #     cursor = conn.cursor()
# #     query = """UPDATE employee SET name = %s, department = %s, phone_no1 = %s, phone_no2 = %s,
# #                designation = %s, linkedin_link = %s, service_provided = %s, company = %s WHERE id = %s"""
# #     values = (name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company, id)
# #     cursor.execute(query, values)
# #     conn.commit()
# #     conn.close()
# #     return True
# #
# # # Fetch Service Data
# # def fetch_service_data():
# #     """Fetch service data from the MySQL database."""
# #     conn = mysql.connector.connect(host="localhost", user="root", password=DB_PASSWORD, database="crm")
# #     cursor = conn.cursor()
# #     cursor.execute("SELECT service_provided FROM employee")
# #     services = [row[0] for row in cursor.fetchall()]
# #     conn.close()
# #     return services
# #
# #
# #
#
#
# import mysql.connector
# from mysql.connector import connect, Error
# from tkinter import messagebox
#
# DB_PASSWORD = 'root@1234567890'
#
#
# # Database Connection
# def connect_to_db():
#     """
#     Establish a connection to the MySQL database.
#     """
#     try:
#         return connect(
#             host="localhost",
#             user="root",
#             password=DB_PASSWORD,
#             database="crm"
#         )
#     except mysql.connector.Error as err:
#         messagebox.showerror("Database Error", f"Error: {err}")
#         return None
#
#
# # Fetch Data for Analysis
# def fetch_data(field):
#     """Fetch data from the database based on the selected field."""
#     conn = connect_to_db()
#     if conn:
#         try:
#             cursor = conn.cursor()
#             query = f"SELECT {field} FROM employee"
#             cursor.execute(query)
#             data = [row[0] for row in cursor.fetchall()]
#             return data
#         finally:
#             conn.close()
#     return []
#
#
# # User Registration and Login
# def save_registration_data(name, email, username, password):
#     conn = connect_to_db()
#     if conn:
#         try:
#             cursor = conn.cursor()
#             sql = "INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)"
#             cursor.execute(sql, (name, email, username, password))
#             conn.commit()
#             messagebox.showinfo("Success", "Registration data saved successfully!")
#         except mysql.connector.Error as err:
#             messagebox.showerror("Database Error", f"Error: {err}")
#         finally:
#             conn.close()
#
#
# def validate_login(username, password):
#     conn = connect_to_db()
#     if conn:
#         try:
#             cursor = conn.cursor()
#             sql = "SELECT * FROM users WHERE username = %s AND password = %s"
#             cursor.execute(sql, (username, password))
#             return cursor.fetchone()
#         except Error as err:
#             messagebox.showerror("Database Error", f"Error: {err}")
#             return None
#         finally:
#             conn.close()
#
#
# # Company CRUD Operations
# def insert_company_data(company_id, company_name, contact_no, primary_business, secondary_business, since, email,
#                         website):
#     conn = connect_to_db()
#     if conn:
#         cursor = conn.cursor()
#         sql = """INSERT INTO company (company_id, company_name, contact_no, primary_business, secondary_business, since, email, website)
#                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
#         values = (company_id, company_name, contact_no, primary_business, secondary_business, since, email, website)
#         try:
#             cursor.execute(sql, values)
#             conn.commit()
#             return True
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
#             return False
#         finally:
#             cursor.close()
#             conn.close()
#     return False
#
#
# def fetch_companies():
#     conn = connect_to_db()
#     if conn:
#         try:
#             cursor = conn.cursor(dictionary=True)
#             cursor.execute(
#                 "SELECT company_id, company_name, contact_no, primary_business, secondary_business, since, email, website FROM company")
#             companies = cursor.fetchall()
#             return companies
#         finally:
#             cursor.close()
#             conn.close()
#     return []
#
#
# def delete_company(company_id):
#     conn = connect_to_db()
#     if conn:
#         cursor = conn.cursor()
#         sql = "DELETE FROM company WHERE company_id = %s"
#         try:
#             cursor.execute(sql, (company_id,))
#             conn.commit()
#             return True
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
#             return False
#         finally:
#             cursor.close()
#             conn.close()
#     return False
#
#
# def update_company(company_id, company_name, contact_no, primary_business, secondary_business, since, email, website):
#     conn = connect_to_db()
#     if conn:
#         cursor = conn.cursor()
#         sql = """
#             UPDATE company SET company_name=%s, contact_no=%s, primary_business=%s, secondary_business=%s, since=%s, email=%s, website=%s
#             WHERE company_id=%s
#         """
#         values = (company_name, contact_no, primary_business, secondary_business, since, email, website, company_id)
#         try:
#             cursor.execute(sql, values)
#             conn.commit()
#             return cursor.rowcount > 0  # Return True if update was successful
#         except Exception as e:
#             print("Error updating company:", e)
#             return False
#         finally:
#             cursor.close()
#             conn.close()
#     return False
#
#
# # New Bulk Insert Function for Companies
# def insert_bulk_company_data(companies):
#     """
#     Insert multiple company records into the company table.
#     Args:
#         companies (list): List of dictionaries containing company data.
#     Returns:
#         bool: True if successful, False otherwise.
#     """
#     conn = connect_to_db()
#     if not conn:
#         return False
#
#     cursor = conn.cursor()
#     sql = """INSERT INTO company (company_id, company_name, contact_no, primary_business, secondary_business, since, email, website)
#              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
#
#     try:
#         # Prepare values for bulk insertion
#         values = [
#             (
#                 company.get('company_id'),
#                 company.get('company_name'),
#                 company.get('contact_no'),
#                 company.get('primary_business', ''),
#                 company.get('secondary_business', ''),
#                 company.get('since', ''),
#                 company.get('email', ''),
#                 company.get('website', '')
#             )
#             for company in companies
#         ]
#
#         # Execute multiple insert statements efficiently
#         cursor.executemany(sql, values)
#         conn.commit()
#         return True
#     except mysql.connector.Error as err:
#         print(f"Error during bulk insert: {err}")
#         return False
#     finally:
#         cursor.close()
#         conn.close()
#
#
# # Employee CRUD Operations
# def fetch_employees():
#     conn = connect_to_db()
#     if conn:
#         try:
#             cursor = conn.cursor(dictionary=True)
#             cursor.execute("SELECT * FROM employee")
#             employees = cursor.fetchall()
#             return employees
#         finally:
#             conn.close()
#     return []
#
#
# def insert_employee(id, name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company):
#     conn = connect_to_db()
#     if conn:
#         cursor = conn.cursor()
#         query = """INSERT INTO employee (id, name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company)
#                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#         values = (id, name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company)
#         try:
#             cursor.execute(query, values)
#             conn.commit()
#             return True
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
#             return False
#         finally:
#             conn.close()
#     return False
#
#
# def delete_employee(id):
#     conn = connect_to_db()
#     if conn:
#         cursor = conn.cursor()
#         query = "DELETE FROM employee WHERE id = %s"
#         try:
#             cursor.execute(query, (id,))
#             conn.commit()
#             return True
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
#             return False
#         finally:
#             conn.close()
#     return False
#
#
# def update_employee(id, company_name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided,
#                     company):
#     conn = connect_to_db()
#     if conn:
#         cursor = conn.cursor()
#         query = """UPDATE employee SET name = %s, department = %s, phone_no1 = %s, phone_no2 = %s,
#                    designation = %s, linkedin_link = %s, service_provided = %s, company = %s
#                    WHERE id = %s"""
#         values = (
#         company_name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company, id)
#         try:
#             cursor.execute(query, values)
#             conn.commit()
#             return True
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
#             return False
#         finally:
#             conn.close()
#     return False
#
#
# # Fetch Service Data
# def fetch_service_data():
#     """Fetch service data from the MySQL database."""
#     conn = connect_to_db()
#     if conn:
#         try:
#             cursor = conn.cursor()
#             cursor.execute("SELECT service_provided FROM employee")
#             services = [row[0] for row in cursor.fetchall()]
#             return services
#         finally:
#             conn.close()
#     return []



import mysql.connector
from mysql.connector import connect, Error
from tkinter import messagebox

DB_PASSWORD = 'root@1234567890'

# Database Connection
def connect_to_db():
    """
    Establish a connection to the MySQL database.
    """
    try:
        return connect(
            host="localhost",
            user="root",
            password=DB_PASSWORD,
            database="crm"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Fetch Data for Analysis
def fetch_data(field):
    """Fetch data from the database based on the selected field."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = f"SELECT {field} FROM employee"
            cursor.execute(query)
            data = [row[0] for row in cursor.fetchall()]
            return data
        finally:
            conn.close()
    return []

# User Registration and Login
def save_registration_data(name, email, username, password):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, email, username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration data saved successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            conn.close()

def validate_login(username, password):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            return cursor.fetchone()
        except Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return None
        finally:
            conn.close()

# Company CRUD Operations
def insert_company_data(company_id, company_name, contact_no, primary_business, secondary_business, since, email,
                        website):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        sql = """INSERT INTO company (company_id, company_name, contact_no, primary_business, secondary_business, since, email, website) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (company_id, company_name, contact_no, primary_business, secondary_business, since, email, website)
        try:
            cursor.execute(sql, values)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def fetch_companies():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT company_id, company_name, contact_no, primary_business, secondary_business, since, email, website FROM company")
            companies = cursor.fetchall()
            return companies
        finally:
            cursor.close()
            conn.close()
    return []

def delete_company(company_id):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        sql = "DELETE FROM company WHERE company_id = %s"
        try:
            cursor.execute(sql, (company_id,))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def update_company(company_id, company_name, contact_no, primary_business, secondary_business, since, email, website):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        sql = """
            UPDATE company SET company_name=%s, contact_no=%s, primary_business=%s, secondary_business=%s, since=%s, email=%s, website=%s 
            WHERE company_id=%s
        """
        values = (company_name, contact_no, primary_business, secondary_business, since, email, website, company_id)
        try:
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0  # Return True if update was successful
        except Exception as e:
            print("Error updating company:", e)
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def insert_bulk_company_data(companies):
    """
    Insert multiple company records into the company table.
    Args:
        companies (list): List of dictionaries containing company data.
    Returns:
        bool: True if successful, False otherwise.
    """
    conn = connect_to_db()
    if not conn:
        return False

    cursor = conn.cursor()
    sql = """INSERT INTO company (company_id, company_name, contact_no, primary_business, secondary_business, since, email, website) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    try:
        values = [
            (
                company.get('company_id'),
                company.get('company_name'),
                company.get('contact_no'),
                company.get('primary_business', ''),
                company.get('secondary_business', ''),
                company.get('since', ''),
                company.get('email', ''),
                company.get('website', '')
            )
            for company in companies
        ]
        cursor.executemany(sql, values)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error during bulk insert: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# Employee CRUD Operations
def fetch_employees():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employee")
            employees = cursor.fetchall()
            return employees
        finally:
            conn.close()
    return []

def insert_employee(id, name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = """INSERT INTO employee (id, name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (id, name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company)
        try:
            cursor.execute(query, values)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            conn.close()
    return False

def delete_employee(id):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "DELETE FROM employee WHERE id = %s"
        try:
            cursor.execute(query, (id,))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            conn.close()
    return False

def update_employee(id, name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = """UPDATE employee SET name = %s, department = %s, phone_no1 = %s, phone_no2 = %s, 
                   designation = %s, linkedin_link = %s, service_provided = %s, company = %s 
                   WHERE id = %s"""
        values = (name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company, id)
        try:
            cursor.execute(query, values)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            conn.close()
    return False

def insert_bulk_employee_data(employees):
    """
    Insert multiple employee records into the employee table.
    Args:
        employees (list): List of dictionaries containing employee data.
    Returns:
        bool: True if successful, False otherwise.
    """
    conn = connect_to_db()
    if not conn:
        return False

    cursor = conn.cursor()
    sql = """INSERT INTO employee (id, name, department, phone_no1, phone_no2, designation, linkedin_link, service_provided, company) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    try:
        values = [
            (
                employee.get('id'),
                employee.get('name'),
                employee.get('department'),
                employee.get('phone_no1'),
                employee.get('phone_no2', ''),
                employee.get('designation', ''),
                employee.get('linkedin_link', ''),
                employee.get('service_provided', ''),
                employee.get('company')
            )
            for employee in employees
        ]
        cursor.executemany(sql, values)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error during bulk employee insert: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# Fetch Service Data
def fetch_service_data():
    """Fetch service data from the MySQL database."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT service_provided FROM employee")
            services = [row[0] for row in cursor.fetchall()]
            return services
        finally:
            conn.close()
    return []
