# app_frontend.py
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# API URL
API_BASE_URL = "http://localhost:5555/api"

# State management
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None

# Page title
st.title("Expense Tracker")

# Login/Registration Section
if not st.session_state.token:
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.header("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/auth/login",
                    json={"username": username, "password": password}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.token = data['token']
                    st.session_state.user = data['user']
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(f"Login failed: {response.json().get('message', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with tab2:
        st.header("Register")
        new_username = st.text_input("Username", key="reg_username")
        new_email = st.text_input("Email", key="reg_email")
        new_password = st.text_input("Password", type="password", key="reg_password")
        
        if st.button("Register"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/auth/register",
                    json={
                        "username": new_username,
                        "email": new_email,
                        "password": new_password
                    }
                )
                
                if response.status_code == 201:
                    st.success("Registration successful! You can now login.")
                else:
                    st.error(f"Registration failed: {response.json().get('message', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
else:
    # Logout button
    col1, col2 = st.columns([9, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
    
    with col1:
        st.write(f"Welcome, **{st.session_state.user['username']}**!")
    
    # Expense Management
    tab1, tab2 = st.tabs(["View Expenses", "Add Expense"])
    
    # Helper function to get expenses
    def get_expenses(filter_type='all', start_date=None, end_date=None):
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        params = {"filter": filter_type}
        
        if filter_type == 'custom' and start_date and end_date:
            params["start_date"] = start_date.isoformat()
            params["end_date"] = end_date.isoformat()
            
        response = requests.get(f"{API_BASE_URL}/expenses/", headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()['expenses']
        else:
            st.error(f"Failed to fetch expenses: {response.json().get('message', 'Unknown error')}")
            return []
    
    with tab1:
        st.header("Your Expenses")
        
        # Filter options
        filter_option = st.selectbox(
            "Filter by time period:",
            ["All", "Past Week", "Past Month", "Past 3 Months", "Custom Date Range"]
        )
        
        filter_map = {
            "All": "all",
            "Past Week": "week",
            "Past Month": "month",
            "Past 3 Months": "three_months",
            "Custom Date Range": "custom"
        }
        
        if filter_option == "Custom Date Range":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
            with col2:
                end_date = st.date_input("End Date", datetime.now())
                
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())
            
            expenses = get_expenses("custom", start_datetime, end_datetime)
        else:
            expenses = get_expenses(filter_map[filter_option])
        
        if expenses:
            # Convert to DataFrame for better display
            df = pd.DataFrame(expenses)
            
            # Format the DataFrame
            if not df.empty:
                df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M')
                df = df[['title', 'amount', 'category', 'date', 'description', 'id']]
                df.columns = ['Title', 'Amount', 'Category', 'Date', 'Description', 'ID']
                
                st.dataframe(df, use_container_width=True)
                
                # Total amount
                total = df['Amount'].sum()
                st.metric("Total Amount", f"${total:.2f}")
                
                # Edit/Delete expense
                col1, col2 = st.columns(2)
                with col1:
                    expense_id = st.number_input("Enter Expense ID to Edit/Delete", min_value=1, step=1)
                
                with col2:
                    action = st.selectbox("Action", ["Edit", "Delete"])
                
                if action == "Edit" and st.button("Proceed with Edit"):
                    # Get the expense details
                    expense_to_edit = next((e for e in expenses if e['id'] == expense_id), None)
                    if expense_to_edit:
                        st.session_state.editing_expense = expense_to_edit
                        st.session_state.editing = True
                        st.rerun()
                    else:
                        st.error("Expense not found!")
                
                elif action == "Delete" and st.button("Proceed with Delete"):
                    try:
                        headers = {"Authorization": f"Bearer {st.session_state.token}"}
                        response = requests.delete(
                            f"{API_BASE_URL}/expenses/{expense_id}",
                            headers=headers
                        )
                        
                        if response.status_code == 200:
                            st.success("Expense deleted successfully!")
                            st.rerun()
                        else:
                            st.error(f"Failed to delete expense: {response.json().get('message', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            st.info("No expenses found for the selected time period.")
    
    # Edit expense form
    if 'editing' in st.session_state and st.session_state.editing:
        st.header("Edit Expense")
        expense = st.session_state.editing_expense
        
        title = st.text_input("Title", value=expense['title'])
        amount = st.number_input("Amount", value=float(expense['amount']), min_value=0.01, step=0.01)
        category = st.selectbox(
            "Category",
            ["GROCERIES", "LEISURE", "ELECTRONICS", "UTILITIES", "CLOTHING", "HEALTH", "OTHERS"],
            index=["GROCERIES", "LEISURE", "ELECTRONICS", "UTILITIES", "CLOTHING", "HEALTH", "OTHERS"].index(expense['category'])
        )
        date = st.date_input("Date", pd.to_datetime(expense['date']).date())
        description = st.text_area("Description", value=expense['description'] if expense['description'] else "")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Update Expense"):
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.token}"}
                    # Convert date to datetime with time from the original expense
                    original_time = pd.to_datetime(expense['date']).time()
                    updated_datetime = datetime.combine(date, original_time)
                    
                    response = requests.put(
                        f"{API_BASE_URL}/expenses/{expense['id']}",
                        headers=headers,
                        json={
                            "title": title,
                            "amount": amount,
                            "category": category,
                            "date": updated_datetime.isoformat(),
                            "description": description
                        }
                    )
                    
                    if response.status_code == 200:
                        st.success("Expense updated successfully!")
                        st.session_state.editing = False
                        st.rerun()
                    else:
                        st.error(f"Failed to update expense: {response.json().get('message', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col2:
            if st.button("Cancel"):
                st.session_state.editing = False
                st.rerun()
    
    with tab2:
        st.header("Add New Expense")
        
        # Form inputs
        title = st.text_input("Title")
        amount = st.number_input("Amount", min_value=0.01, step=0.01)
        category = st.selectbox("Category", ["GROCERIES", "LEISURE", "ELECTRONICS", "UTILITIES", "CLOTHING", "HEALTH", "OTHERS"])
        date = st.date_input("Date")
        time_input = st.time_input("Time")
        description = st.text_area("Description")
        
        if st.button("Add Expense"):
            try:
                # Combine date and time
                expense_datetime = datetime.combine(date, time_input)
                
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                response = requests.post(
                    f"{API_BASE_URL}/expenses/",
                    headers=headers,
                    json={
                        "title": title,
                        "amount": amount,
                        "category": category,
                        "date": expense_datetime.isoformat(),
                        "description": description
                    }
                )
                
                if response.status_code == 201:
                    st.success("Expense added successfully!")
                    # Clear form
                    st.text_input("Title", value="")
                    st.number_input("Amount", value=0.0, min_value=0.01, step=0.01)
                    st.text_area("Description", value="")
                    st.rerun()
                else:
                    st.error(f"Failed to add expense: {response.json().get('message', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    # Run with: streamlit run app_frontend.py
    pass