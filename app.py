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
from translations import get_text

st.set_page_config(
    page_title="Maktab Financial Dashboard",
    page_icon="🕌",
    layout="wide"
)

def initialize_session_state():
    if 'language' not in st.session_state:
        st.session_state.language = 'bn'

def language_selector():
    languages = {
        'বাংলা': 'bn',
        'English': 'en'
    }
    current_lang_name = [k for k, v in languages.items() if v == st.session_state.language][0]
    
    with st.sidebar:
        selected_lang = st.selectbox(
            "🌐 ভাষা/Language",
            options=list(languages.keys()),
            index=list(languages.keys()).index(current_lang_name)
        )
        if languages[selected_lang] != st.session_state.language:
            st.session_state.language = languages[selected_lang]
            st.rerun()

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
    # Rename columns to more readable names using translations
    column_map = {
        'donor_name': get_text('column_donor_name', st.session_state.language),
        'display_name': get_text('column_display_name', st.session_state.language),
        'teacher_name': get_text('column_teacher_name', st.session_state.language),
        'description': get_text('column_description', st.session_state.language),
        'amount': get_text('column_amount', st.session_state.language),
        'date': get_text('column_date', st.session_state.language),
        'notes': get_text('column_notes', st.session_state.language),
        'category': get_text('column_category', st.session_state.language),
        'is_anonymous': get_text('column_is_anonymous', st.session_state.language)
    }
    df = df.rename(columns={k: v for k, v in column_map.items() if k in df.columns})
    
    # Format date
    date_column = get_text('column_date', st.session_state.language)
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column]).dt.strftime('%d %B, %Y')
    
    # Format amount
    amount_column = get_text('column_amount', st.session_state.language)
    if amount_column in df.columns:
        df[amount_column] = df[amount_column].apply(format_currency)
    
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
    initialize_session_state()
    language_selector()
    
    st.title(get_text('title', st.session_state.language))
    
    # Add login/logout in sidebar
    with st.sidebar:
        if check_admin_auth():
            if st.button(get_text('logout', st.session_state.language)):
                st.session_state.is_admin = False
                st.rerun()
            st.success(get_text('logged_in', st.session_state.language))
        else:
            st.warning(get_text('view_only', st.session_state.language))
            if st.button(get_text('admin_login', st.session_state.language)):
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
    st.header(get_text('financial_overview', st.session_state.language))
    
    # Summary cards
    col1, col2, col3 = st.columns(3)
    
    # Summary statistics
    donations = get_all_donations()
    expenses = get_all_expenses()
    salaries = get_teacher_salaries()
    
    total_donations = sum(d['amount'] for d in donations) if donations else 0
    total_expenses = sum(e['amount'] for e in expenses) if expenses else 0
    total_salaries = sum(s['amount'] for s in salaries) if salaries else 0
    
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
        st.metric(get_text('total_donations', st.session_state.language), format_currency(total_donations))
    with col2:
        st.metric(get_text('total_expenses', st.session_state.language), format_currency(total_expenses))
    with col3:
        st.metric(get_text('total_salaries', st.session_state.language), format_currency(total_salaries))
    
    # Monthly trends chart - Commented out
    # st.subheader(get_text('monthly_trends', st.session_state.language))
    # if donations:  # Only show chart if there are donations
    #     df_donations = pd.DataFrame(donations)
    #     df_donations['date'] = pd.to_datetime(df_donations['date'])
    #     monthly_donations = df_donations.groupby(df_donations['date'].dt.strftime('%Y-%m'))[['amount']].sum()
    #     fig = px.line(monthly_donations, 
    #                  title="Monthly Donations",
    #                  labels={'value': 'Amount (৳)', 'index': 'Month'},
    #                  template="plotly_white")
    #     fig.update_traces(line_color="#2ecc71", line_width=3)
    #     st.plotly_chart(fig, use_container_width=True)
    # else:
    #     st.info(get_text('no_donations_data', st.session_state.language))
    
    # Display all data tables
    col1, col2 = st.columns(2)
    
    with col1:
        # Recent Donations
        st.subheader(get_text('recent_donations', st.session_state.language))
        if donations:
            df_donations = pd.DataFrame(donations)
            
            # Modify display for donations based on user type and anonymous status
            if check_admin_auth():
                # Admins see all donor names
                display_df = style_dataframe(df_donations[['donor_name', 'amount', 'date', 'notes']])
            else:
                # Regular users see anonymous names only for anonymous donations
                df_donations['display_name'] = df_donations.apply(
                    lambda x: get_text('anonymous_donor', st.session_state.language) if x['is_anonymous'] 
                    else x['donor_name'], axis=1
                )
                display_df = style_dataframe(df_donations[['display_name', 'amount', 'date', 'notes']])
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info(get_text('no_donations', st.session_state.language))
        
        # Teacher Salaries
        st.subheader(get_text('teacher_salaries', st.session_state.language))
        if salaries:
            df_salaries = pd.DataFrame(salaries)
            display_df = style_dataframe(df_salaries[['teacher_name', 'amount', 'date']])
            
            # Teacher-wise summary
            teacher_summary = df_salaries.groupby('teacher_name')['amount'].sum().reset_index()
            teacher_summary['amount'] = teacher_summary['amount'].apply(format_currency)
            
            # Display summary
            for teacher, amount in zip(teacher_summary['teacher_name'], teacher_summary['amount']):
                st.metric(f"Total for {teacher}", amount)
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info(get_text('no_salaries', st.session_state.language))
    
    with col2:
        # Recent Expenses
        st.subheader(get_text('expenses', st.session_state.language))
        if expenses:
            df_expenses = pd.DataFrame(expenses)
            display_df = style_dataframe(df_expenses[['description', 'amount', 'date', 'category']])
            
            # Category-wise summary
            category_summary = df_expenses.groupby('category')['amount'].sum().reset_index()
            category_summary['amount'] = category_summary['amount'].apply(format_currency)
            
            # Display category summary
            for cat, amount in zip(category_summary['category'], category_summary['amount']):
                st.metric(f"Total {cat}", amount)
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info(get_text('no_expenses', st.session_state.language))
    
    # Add some spacing
    st.markdown("---")
    
    # Additional Statistics
    st.subheader(get_text('quick_stats', st.session_state.language))
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        num_donors = len(pd.DataFrame(donations)['donor_name'].unique()) if donations else 0
        st.metric(get_text('num_donors', st.session_state.language), num_donors)
    with col2:
        num_teachers = len(pd.DataFrame(salaries)['teacher_name'].unique()) if salaries else 0
        st.metric(get_text('num_teachers', st.session_state.language), num_teachers)
    with col3:
        expense_categories = len(pd.DataFrame(expenses)['category'].unique()) if expenses else 0
        st.metric(get_text('expense_cats', st.session_state.language), expense_categories)
    with col4:
        current_balance = total_donations - (total_expenses + total_salaries)
        st.metric(get_text('current_balance', st.session_state.language), format_currency(current_balance))

def show_donations():
    st.header(get_text('donations', st.session_state.language))
    
    # Only show the donation form to admin users
    if check_admin_auth():
        with st.form("donation_form"):
            st.subheader(get_text('add_donation', st.session_state.language))
            donor_name = st.text_input(get_text('donor_name', st.session_state.language))
            amount = st.number_input("Amount (৳)", min_value=0.0)
            date = st.date_input("Date")
            notes = st.text_area("Notes")
            is_anonymous = st.checkbox(get_text('anonymous_donation', st.session_state.language))
            
            if st.form_submit_button("Add Donation"):
                add_donation(donor_name, amount, date, notes, is_anonymous)
                st.success("Donation added successfully!")
                st.rerun()
    
    # Display donations table
    donations = get_all_donations()
    if donations:
        df = pd.DataFrame(donations)
        
        # Show edit/delete options for admin
        if check_admin_auth():
            st.subheader("Edit Donations")
            for index, row in df.iterrows():
                with st.expander(f"Donation: {row['donor_name']} - ৳{row['amount']:,.2f} ({row['date']})"):
                    with st.form(f"edit_donation_{row['id']}"):
                        new_donor = st.text_input("Donor Name", row['donor_name'])
                        new_amount = st.number_input("Amount (৳)", value=float(row['amount']), min_value=0.0)
                        new_date = st.date_input("Date", pd.to_datetime(row['date']))
                        new_notes = st.text_area("Notes", row['notes'] if row['notes'] else "")
                        new_anonymous = st.checkbox("Anonymous", value=row['is_anonymous'])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("Update"):
                                update_donation(row['id'], new_donor, new_amount, new_date, new_notes, new_anonymous)
                                st.success("Updated successfully!")
                                st.rerun()
                        with col2:
                            if st.form_submit_button("Delete", type="secondary"):
                                delete_donation(row['id'])
                                st.success("Deleted successfully!")
                                st.rerun()
        
        # Display table for all users
        st.subheader("All Donations")
        if check_admin_auth():
            display_columns = ['donor_name', 'amount', 'date', 'notes', 'is_anonymous']
        else:
            df['display_name'] = df.apply(
                lambda x: get_text('anonymous_donor', st.session_state.language) if x['is_anonymous'] 
                else x['donor_name'], axis=1
            )
            display_columns = ['display_name', 'amount', 'date', 'notes']
        
        display_df = style_dataframe(df[display_columns])
        st.dataframe(display_df, use_container_width=True, hide_index=True)

def show_expenses():
    st.header(get_text('expenses', st.session_state.language))
    
    if check_admin_auth():
        with st.form("expense_form"):
            st.subheader(get_text('add_new_expense', st.session_state.language))
            description = st.text_input("Description")
            amount = st.number_input("Amount (৳)", min_value=0.0)
            date = st.date_input("Date")
            category = st.selectbox("Category", ["Utilities", "Supplies", "Maintenance", "Other"])
            
            if st.form_submit_button("Add Expense"):
                add_expense(description, amount, date, category)
                st.success("Expense added successfully!")
                st.rerun()
    
    expenses = get_all_expenses()
    if expenses:
        df = pd.DataFrame(expenses)
        
        # Show edit/delete options for admin
        if check_admin_auth():
            st.subheader("Edit Expenses")
            for index, row in df.iterrows():
                with st.expander(f"Expense: {row['description']} - ৳{row['amount']:,.2f} ({row['date']})"):
                    with st.form(f"edit_expense_{row['id']}"):
                        new_desc = st.text_input("Description", row['description'])
                        new_amount = st.number_input("Amount (৳)", value=float(row['amount']), min_value=0.0)
                        new_date = st.date_input("Date", pd.to_datetime(row['date']))
                        new_category = st.selectbox("Category", 
                                                  ["Utilities", "Supplies", "Maintenance", "Other"],
                                                  index=["Utilities", "Supplies", "Maintenance", "Other"].index(row['category']))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("Update"):
                                update_expense(row['id'], new_desc, new_amount, new_date, new_category)
                                st.success("Updated successfully!")
                                st.rerun()
                        with col2:
                            if st.form_submit_button("Delete", type="secondary"):
                                delete_expense(row['id'])
                                st.success("Deleted successfully!")
                                st.rerun()
        
        # Display table for all users
        st.subheader("All Expenses")
        display_df = style_dataframe(df[['description', 'amount', 'date', 'category']])
        st.dataframe(display_df, use_container_width=True, hide_index=True)

def show_teacher_salaries():
    st.header(get_text('teacher_salaries', st.session_state.language))
    
    if check_admin_auth():
        with st.form("salary_form"):
            st.subheader("Add Salary Payment")
            teacher_name = st.text_input("Teacher Name")
            amount = st.number_input("Amount (৳)", min_value=0.0)
            date = st.date_input("Date")
            
            if st.form_submit_button("Add Salary Payment"):
                add_salary(teacher_name, amount, date)
                st.success("Salary payment added successfully!")
                st.rerun()
    
    salaries = get_teacher_salaries()
    if salaries:
        df = pd.DataFrame(salaries)
        
        # Show edit/delete options for admin
        if check_admin_auth():
            st.subheader("Edit Salary Payments")
            for index, row in df.iterrows():
                with st.expander(f"Salary: {row['teacher_name']} - ৳{row['amount']:,.2f} ({row['date']})"):
                    with st.form(f"edit_salary_{row['id']}"):
                        new_teacher = st.text_input("Teacher Name", row['teacher_name'])
                        new_amount = st.number_input("Amount (৳)", value=float(row['amount']), min_value=0.0)
                        new_date = st.date_input("Date", pd.to_datetime(row['date']))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("Update"):
                                update_salary(row['id'], new_teacher, new_amount, new_date)
                                st.success("Updated successfully!")
                                st.rerun()
                        with col2:
                            if st.form_submit_button("Delete", type="secondary"):
                                delete_salary(row['id'])
                                st.success("Deleted successfully!")
                                st.rerun()
        
        # Display table for all users
        st.subheader("All Salary Payments")
        display_df = style_dataframe(df[['teacher_name', 'amount', 'date']])
        st.dataframe(display_df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main() 