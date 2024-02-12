import streamlit as st
import sqlite3

# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

# Function to create user table
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# Function to add a new user
def add_user(conn, name):
    sql = ''' INSERT INTO users(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (name,))
    conn.commit()
    return cur.lastrowid

# Function to add expense
def add_expense(conn, user_id, category, amount):
    sql = ''' INSERT INTO expenses(user_id, category, amount)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (user_id, category, amount))
    conn.commit()
    return cur.lastrowid

# Function to get expenses by user
def get_expenses_by_user(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE user_id=?", (user_id,))
    rows = cur.fetchall()
    return rows

# Main function
def main():
    # Title
    st.title("Expense Tracker")

    # Create or connect to the database
    conn = create_connection("expense_tracker.db")

    # Create users table if it doesn't exist
    create_table_sql = """ CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL
                                ); """
    if conn is not None:
        create_table(conn, create_table_sql)
    else:
        st.error("Error! cannot create the database connection.")

    # Sidebar
    menu = ["Home", "Add Expense", "View Expenses"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Add Expense":
        st.subheader("Add Expense")
        name = st.text_input("Enter your name")
        user_id = add_user(conn, name) if name else None

        if user_id:
            category = st.selectbox("Select Category", ["Food", "Transport", "Shopping", "Others"])
            amount = st.number_input("Enter Amount")
            if st.button("Add Expense"):
                add_expense(conn, user_id, category, amount)
                st.success("Expense added successfully!")

    elif choice == "View Expenses":
        st.subheader("View Expenses")
        name = st.text_input("Enter your name")
        user_id = add_user(conn, name) if name else None

        if user_id:
            expenses = get_expenses_by_user(conn, user_id)
            if expenses:
                st.write("Your Expenses:")
                for expense in expenses:
                    st.write(f"Category: {expense[2]}, Amount: {expense[3]}")
            else:
                st.write("No expenses found.")

if __name__ == '__main__':
    main()
