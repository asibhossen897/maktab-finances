import os
from typing import List
import bcrypt
import streamlit as st
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime
from models import Donation, Expense, Salary, AdminUser
from config import SUPABASE_DB_URL
from db_config import POOL_CONFIG

# Create engine with Supabase connection
engine = create_engine(
    SUPABASE_DB_URL,
    echo=False,
    **POOL_CONFIG
)

def init_db():
    """Initialize the database, creating all tables"""
    SQLModel.metadata.create_all(engine)
    
    # Add default admin user if none exists
    with Session(engine) as session:
        admin_exists = session.exec(select(AdminUser)).first()
        if not admin_exists:
            default_username = st.secrets.get("ADMIN_USERNAME", "admin")
            default_password = st.secrets.get("ADMIN_PASSWORD", "admin123")
            
            # Hash the password
            password_bytes = default_password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password_bytes, salt)
            
            # Create admin user
            admin = AdminUser(username=default_username, password_hash=hashed_password)
            session.add(admin)
            session.commit()

def hash_password(password: str) -> bytes:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt)

def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def add_donation(donor_name: str, amount: float, date: datetime, notes: str, is_anonymous: bool = False):
    with Session(engine) as session:
        donation = Donation(
            donor_name=donor_name,
            amount=amount,
            date=date,
            notes=notes,
            is_anonymous=is_anonymous
        )
        session.add(donation)
        session.commit()

def add_expense(description: str, amount: float, date: datetime, category: str):
    with Session(engine) as session:
        expense = Expense(
            description=description,
            amount=amount,
            date=date,
            category=category
        )
        session.add(expense)
        session.commit()

def add_salary(teacher_name: str, amount: float, date: datetime):
    with Session(engine) as session:
        salary = Salary(
            teacher_name=teacher_name,
            amount=amount,
            date=date
        )
        session.add(salary)
        session.commit()

def get_all_donations() -> List[dict]:
    with Session(engine) as session:
        donations = session.exec(select(Donation).order_by(Donation.date.desc())).all()
        return [donation.dict() for donation in donations]

def get_all_expenses() -> List[dict]:
    with Session(engine) as session:
        expenses = session.exec(select(Expense).order_by(Expense.date.desc())).all()
        return [expense.dict() for expense in expenses]

def get_teacher_salaries() -> List[dict]:
    with Session(engine) as session:
        salaries = session.exec(select(Salary).order_by(Salary.date.desc())).all()
        return [salary.dict() for salary in salaries]

def verify_admin(username: str, password: str) -> bool:
    with Session(engine) as session:
        admin = session.exec(
            select(AdminUser).where(AdminUser.username == username)
        ).first()
        
        if admin:
            return check_password(password, admin.password_hash)
    return False

def change_admin_password(username: str, old_password: str, new_password: str) -> bool:
    if verify_admin(username, old_password):
        with Session(engine) as session:
            admin = session.exec(
                select(AdminUser).where(AdminUser.username == username)
            ).first()
            admin.password_hash = hash_password(new_password)
            session.add(admin)
            session.commit()
        return True
    return False

def update_donation(id: int, donor_name: str, amount: float, date: datetime, notes: str, is_anonymous: bool):
    with Session(engine) as session:
        donation = session.get(Donation, id)
        if donation:
            donation.donor_name = donor_name
            donation.amount = amount
            donation.date = date
            donation.notes = notes
            donation.is_anonymous = is_anonymous
            session.add(donation)
            session.commit()

def update_expense(id: int, description: str, amount: float, date: datetime, category: str):
    with Session(engine) as session:
        expense = session.get(Expense, id)
        if expense:
            expense.description = description
            expense.amount = amount
            expense.date = date
            expense.category = category
            session.add(expense)
            session.commit()

def update_salary(id: int, teacher_name: str, amount: float, date: datetime):
    with Session(engine) as session:
        salary = session.get(Salary, id)
        if salary:
            salary.teacher_name = teacher_name
            salary.amount = amount
            salary.date = date
            session.add(salary)
            session.commit()

def delete_donation(id: int):
    with Session(engine) as session:
        donation = session.get(Donation, id)
        if donation:
            session.delete(donation)
            session.commit()

def delete_expense(id: int):
    with Session(engine) as session:
        expense = session.get(Expense, id)
        if expense:
            session.delete(expense)
            session.commit()

def delete_salary(id: int):
    with Session(engine) as session:
        salary = session.get(Salary, id)
        if salary:
            session.delete(salary)
            session.commit()

# Initialize the database when the module is imported
init_db() 