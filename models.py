from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel

class DonationBase(SQLModel):
    donor_name: str
    amount: float = Field(default=0.0)
    date: date
    notes: Optional[str] = None
    is_anonymous: bool = Field(default=False)

class Donation(DonationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ExpenseBase(SQLModel):
    description: str
    amount: float = Field(default=0.0)
    date: date
    category: str

class Expense(ExpenseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class SalaryBase(SQLModel):
    teacher_name: str
    amount: float = Field(default=0.0)
    date: date

class Salary(SalaryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class AdminUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password_hash: bytes 