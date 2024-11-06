import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from database import (
    get_all_donations,
    get_all_expenses,
    get_teacher_salaries,
    add_donation,
    add_expense,
    add_salary,
    verify_admin,
    update_donation,
    update_expense,
    update_salary,
    delete_donation,
    delete_expense,
    delete_salary,
    change_admin_password
)

st.set_page_config(
    page_title="Maktab Financial Dashboard",
    page_icon="🕌",
    layout="wide"
)

def check_admin_auth():
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    return st.session_state.is_admin

def login_page():
    st.title("Admin Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if verify_admin(username, password):
                st.session_state.is_admin = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

def format_currency(value):
    return f"৳{value:,.2f}"

def style_dataframe(df):
    # Rename columns to more readable names
    column_map = {
        'donor_name': 'Donor Name',
        'teacher_name': 'Teacher Name',
        'description': 'Description',
        'amount': 'Amount',
        'date': 'Date',
        'notes': 'Notes',
        'category': 'Category'
    }
    df = df.rename(columns={k: v for k, v in column_map.items() if k in df.columns})
    
    # Format date
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d %B, %Y')
    
    # Format amount
    if 'Amount' in df.columns:
        df['Amount'] = df['Amount'].apply(format_currency)
    
    return df

def show_admin_settings():
    st.header("Admin Settings")
    
    with st.form("change_password_form"):
        st.subheader("Change Password")
        username = st.text_input("Username")
        old_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button("Change Password"):
            if new_password != confirm_password:
                st.error("New passwords don't match!")
            elif len(new_password) < 8:
                st.error("Password must be at least 8 characters long!")
            else:
                if change_admin_password(username, old_password, new_password):
                    st.success("Password changed successfully!")
                    st.session_state.is_admin = False  # Force re-login
                    st.rerun()
                else:
                    st.error("Current password is incorrect!")

def main():
    st.title("Maktab Financial Management System")
    
    # Add login/logout in sidebar
    with st.sidebar:
        if check_admin_auth():
            if st.button("Logout"):
                st.session_state.is_admin = False
                st.rerun()
            st.success("Logged in as Admin")
        else:
            st.warning("View-only mode. Login for admin access.")
            if st.button("Admin Login"):
                st.session_state.current_page = "login"
                st.rerun()
    
    if not check_admin_auth() and st.session_state.get('current_page') == "login":
        login_page()
        return
    
    # Sidebar navigation
    if check_admin_auth():
        page = st.sidebar.selectbox(
            "Select Page",
            ["Dashboard", "Donations", "Expenses", "Teacher Salaries", "Admin Settings"]
        )
    else:
        page = st.sidebar.selectbox(
            "Select Page",
            ["Dashboard", "Donations", "Expenses", "Teacher Salaries"]
        )
    
    if page == "Admin Settings" and check_admin_auth():
        show_admin_settings()
    elif page == "Dashboard":
        show_dashboard()
    elif page == "Donations":
        show_donations()
    elif page == "Expenses":
        show_expenses()
    elif page == "Teacher Salaries":
        show_teacher_salaries()

def show_dashboard():
    st.header("Financial Overview")
    
    col1, col2, col3 = st.columns(3)
    
    # Summary statistics
    donations = get_all_donations()
    expenses = get_all_expenses()
    salaries = get_teacher_salaries()
    
    total_donations = sum(d['amount'] for d in donations)
    total_expenses = sum(e['amount'] for e in expenses)
    total_salaries = sum(s['amount'] for s in salaries)
    
    # Add metric styling
    metric_style = """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #2ecc71;
    }
    </style>
    """
    st.markdown(metric_style, unsafe_allow_html=True)
    
    with col1:
        st.metric("Total Donations", format_currency(total_donations))
    with col2:
        st.metric("Total Expenses", format_currency(total_expenses))
    with col3:
        st.metric("Total Salaries", format_currency(total_salaries))
    
    # Monthly trends chart with improved styling
    st.subheader("Monthly Financial Trends")
    df_donations = pd.DataFrame(donations)
    if not df_donations.empty:
        df_donations['date'] = pd.to_datetime(df_donations['date'])
        monthly_donations = df_donations.groupby(df_donations['date'].dt.strftime('%Y-%m'))[['amount']].sum()
        fig = px.line(monthly_donations, 
                     title="Monthly Donations",
                     labels={'value': 'Amount (৳)', 'index': 'Month'},
                     template="plotly_white")
        fig.update_traces(line_color="#2ecc71", line_width=3)
        st.plotly_chart(fig, use_container_width=True)

def show_donations():
    st.header("Donations Management")
    
    # Only show the donation form to admin users
    if check_admin_auth():
        with st.form("donation_form"):
            st.subheader("Add New Donation")
            donor_name = st.text_input("Donor Name")
            amount = st.number_input("Amount (৳)", min_value=0.0)
            date = st.date_input("Date")
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Add Donation"):
                add_donation(donor_name, amount, date, notes)
                st.success("Donation added successfully!")
    
    # Display donations table with improved formatting
    donations = get_all_donations()
    if donations:
        df = pd.DataFrame(donations)
        if not check_admin_auth():
            # For regular users, show beautifully formatted table
            display_df = style_dataframe(df[['donor_name', 'amount', 'date', 'notes']])
            
            # Add custom CSS for table styling
            st.markdown("""
                <style>
                .dataframe {
                    font-size: 1.1rem;
                    text-align: left;
                }
                .dataframe th {
                    background-color: #2ecc71;
                    color: white;
                    padding: 12px;
                }
                .dataframe td {
                    padding: 12px;
                }
                </style>
            """, unsafe_allow_html=True)
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
            )
            
            # Add summary statistics
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Donations", format_currency(df['amount'].sum()))
            with col2:
                st.metric("Number of Donors", len(df['donor_name'].unique()))

def show_expenses():
    st.header("Expenses Management")
    
    if check_admin_auth():
        with st.form("expense_form"):
            st.subheader("Add New Expense")
            description = st.text_input("Description")
            amount = st.number_input("Amount (৳)", min_value=0.0)
            date = st.date_input("Date")
            category = st.selectbox("Category", ["Utilities", "Supplies", "Maintenance", "Other"])
            
            if st.form_submit_button("Add Expense"):
                add_expense(description, amount, date, category)
                st.success("Expense added successfully!")
    
    expenses = get_all_expenses()
    if expenses:
        df = pd.DataFrame(expenses)
        if not check_admin_auth():
            display_df = style_dataframe(df[['description', 'amount', 'date', 'category']])
            
            # Add category-wise summary
            st.markdown("### Expense Summary by Category")
            category_summary = df.groupby('category')['amount'].sum().reset_index()
            category_summary['amount'] = category_summary['amount'].apply(format_currency)
            
            # Display category summary in columns
            cols = st.columns(len(category_summary))
            for idx, (cat, amount) in enumerate(zip(category_summary['category'], category_summary['amount'])):
                with cols[idx]:
                    st.metric(cat, amount)
            
            st.markdown("### Expense Details")
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
            )

def show_teacher_salaries():
    st.header("Teacher Salaries")
    
    if check_admin_auth():
        with st.form("salary_form"):
            st.subheader("Add Salary Payment")
            teacher_name = st.text_input("Teacher Name")
            amount = st.number_input("Amount (৳)", min_value=0.0)
            date = st.date_input("Date")
            
            if st.form_submit_button("Add Salary Payment"):
                add_salary(teacher_name, amount, date)
                st.success("Salary payment added successfully!")
    
    salaries = get_teacher_salaries()
    if salaries:
        df = pd.DataFrame(salaries)
        if not check_admin_auth():
            display_df = style_dataframe(df[['teacher_name', 'amount', 'date']])
            
            # Add teacher-wise summary
            st.markdown("### Salary Summary by Teacher")
            teacher_summary = df.groupby('teacher_name')['amount'].sum().reset_index()
            teacher_summary['amount'] = teacher_summary['amount'].apply(format_currency)
            
            # Display summary in a grid
            cols = st.columns(min(3, len(teacher_summary)))
            for idx, (teacher, amount) in enumerate(zip(teacher_summary['teacher_name'], teacher_summary['amount'])):
                with cols[idx % 3]:
                    st.metric(teacher, amount)
            
            st.markdown("### Salary Payment Details")
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
            )

if __name__ == "__main__":
    main() 