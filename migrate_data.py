from database import engine as new_engine
from sqlmodel import SQLModel, create_engine, Session, select
from models import Donation, Expense, Salary, AdminUser

# Old SQLite database
old_engine = create_engine("sqlite:///./data/maktab_finance.db")

def migrate_data():
    # Create new tables
    SQLModel.metadata.create_all(new_engine)
    
    with Session(old_engine) as old_session, Session(new_engine) as new_session:
        # Migrate donations
        donations = old_session.exec(select(Donation)).all()
        for donation in donations:
            new_session.add(Donation(**donation.dict()))
        
        # Migrate expenses
        expenses = old_session.exec(select(Expense)).all()
        for expense in expenses:
            new_session.add(Expense(**expense.dict()))
        
        # Migrate salaries
        salaries = old_session.exec(select(Salary)).all()
        for salary in salaries:
            new_session.add(Salary(**salary.dict()))
        
        # Migrate admin users
        admins = old_session.exec(select(AdminUser)).all()
        for admin in admins:
            new_session.add(AdminUser(**admin.dict()))
        
        new_session.commit()

if __name__ == "__main__":
    migrate_data() 