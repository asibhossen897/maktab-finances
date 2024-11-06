import sqlite3
from datetime import datetime
import bcrypt
import os
import streamlit as st

def get_db_connection():
    conn = sqlite3.connect('maktab_finance.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    # Convert the password to bytes and hash it
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt)

def check_password(password, hashed_password):
    # Check if the password matches the hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create donations table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_name TEXT NOT NULL,
            amount REAL NOT NULL,
            date DATE NOT NULL,
            notes TEXT,
            is_anonymous BOOLEAN DEFAULT FALSE
        )
    ''')
    
    # Create expenses table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            date DATE NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    
    # Create salaries table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS salaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_name TEXT NOT NULL,
            amount REAL NOT NULL,
            date DATE NOT NULL
        )
    ''')
    
    # Create admin users table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL
        )
    ''')
    
    # Add a default admin user if none exists
    c.execute('SELECT COUNT(*) FROM admin_users')
    if c.fetchone()[0] == 0:
        # Get admin credentials from streamlit secrets
        default_username = st.secrets.get("ADMIN_USERNAME", "admin")
        default_password = st.secrets.get("ADMIN_PASSWORD", "admin123")
        
        # Hash the password before storing
        hashed_password = hash_password(default_password)
        
        c.execute('''
            INSERT INTO admin_users (username, password_hash)
            VALUES (?, ?)
        ''', (default_username, hashed_password))
    
    conn.commit()
    conn.close()

def add_donation(donor_name, amount, date, notes, is_anonymous=False):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO donations (donor_name, amount, date, notes, is_anonymous)
        VALUES (?, ?, ?, ?, ?)
    ''', (donor_name, amount, date, notes, is_anonymous))
    conn.commit()
    conn.close()

def add_expense(description, amount, date, category):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO expenses (description, amount, date, category)
        VALUES (?, ?, ?, ?)
    ''', (description, amount, date, category))
    conn.commit()
    conn.close()

def add_salary(teacher_name, amount, date):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO salaries (teacher_name, amount, date)
        VALUES (?, ?, ?)
    ''', (teacher_name, amount, date))
    conn.commit()
    conn.close()

def get_all_donations():
    conn = get_db_connection()
    donations = conn.execute('SELECT * FROM donations ORDER BY date DESC').fetchall()
    conn.close()
    return [dict(d) for d in donations]

def get_all_expenses():
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM expenses ORDER BY date DESC').fetchall()
    conn.close()
    return [dict(e) for e in expenses]

def get_teacher_salaries():
    conn = get_db_connection()
    salaries = conn.execute('SELECT * FROM salaries ORDER BY date DESC').fetchall()
    conn.close()
    return [dict(s) for s in salaries]

def verify_admin(username, password):
    conn = get_db_connection()
    user = conn.execute(
        'SELECT password_hash FROM admin_users WHERE username = ?',
        (username,)
    ).fetchone()
    conn.close()
    
    if user:
        stored_hash = user['password_hash']
        return check_password(password, stored_hash)
    return False

def change_admin_password(username, old_password, new_password):
    """Change admin password if old password is correct"""
    if verify_admin(username, old_password):
        conn = get_db_connection()
        new_hash = hash_password(new_password)
        conn.execute(
            'UPDATE admin_users SET password_hash = ? WHERE username = ?',
            (new_hash, username)
        )
        conn.commit()
        conn.close()
        return True
    return False

def update_donation(id, donor_name, amount, date, notes, is_anonymous):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE donations 
        SET donor_name = ?, amount = ?, date = ?, notes = ?, is_anonymous = ?
        WHERE id = ?
    ''', (donor_name, amount, date, notes, is_anonymous, id))
    conn.commit()
    conn.close()

def update_expense(id, description, amount, date, category):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE expenses
        SET description = ?, amount = ?, date = ?, category = ?
        WHERE id = ?
    ''', (description, amount, date, category, id))
    conn.commit()
    conn.close()

def update_salary(id, teacher_name, amount, date):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE salaries
        SET teacher_name = ?, amount = ?, date = ?
        WHERE id = ?
    ''', (teacher_name, amount, date, id))
    conn.commit()
    conn.close()

def delete_donation(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM donations WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def delete_expense(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def delete_salary(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM salaries WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Initialize the database when the module is imported
init_db() 