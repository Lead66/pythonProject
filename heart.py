import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURATION ---
DATA_FILE = "expenses.csv"


def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])


def save_data(df):
    df.to_csv(DATA_FILE, index=False)


# --- UI LAYOUT ---
st.set_page_config(page_title="Python Expense Tracker", layout="centered")
st.title("💰 Personal Expense Tracker")

# Load existing data
df = load_data()

# --- INPUT SECTION ---
with st.expander("➕ Add New Expense"):
    with st.form("expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date", datetime.now())
            category = st.selectbox("Category", ["Food", "Transport", "Rent", "Utilities", "Entertainment", "Other"])
        with col2:
            amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
            description = st.text_input("Description")

        submit = st.form_submit_button("Add Expense")

        if submit:
            new_data = pd.DataFrame([[date, category, description, amount]],
                                    columns=["Date", "Category", "Description", "Amount"])
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(df)
            st.success("Expense added!")

# --- DASHBOARD SECTION ---
if not df.empty:
    st.divider()
    total_spent = df["Amount"].sum()
    st.metric(label="Total Spending", value=f"${total_spent:,.2f}")

    # Show table
    st.subheader("History")
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)

    # Simple Analysis
    st.subheader("Spending by Category")
    category_totals = df.groupby("Category")["Amount"].sum()
    st.bar_chart(category_totals)

if st.button("🗑️ Clear All Data"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            st.rerun()
else:
           st.info("No expenses recorded yet. Start by adding one above!")