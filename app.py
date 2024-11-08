import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import datetime as dt

# Database configuration
db_config = {
    "user": "Buddy",
    "password": "Hirusha_22311",
    "host": "localhost",
    "database": "mydb"
}

# Create a database connection
connection_string = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
engine = create_engine(connection_string)

# Function to load data
@st.cache_data
def load_data():
    query = """
    SELECT o.order_id, o.order_date, o.total_amount, c.customer_id, c.customer_name
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    """
    df = pd.read_sql(query, engine)
    df['order_date'] = pd.to_datetime(df['order_date'])  # Ensure 'order_date' is in datetime format
    return df

# Load data
data = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Date range filter
start_date, end_date = st.sidebar.date_input("Select Order Date Range",
                                             [dt.date(2023, 1, 1), dt.date.today()])

# Filter data by selected date range
filtered_data = data[(data['order_date'] >= pd.to_datetime(start_date)) &
                     (data['order_date'] <= pd.to_datetime(end_date))]

# Slider for total amount spent
min_total_amount = st.sidebar.slider("Minimum Total Amount Spent", 0, 5000, 1000)
customer_totals = filtered_data.groupby('customer_id')['total_amount'].sum()
filtered_customer_ids = customer_totals[customer_totals >= min_total_amount].index
filtered_data = filtered_data[filtered_data['customer_id'].isin(filtered_customer_ids)]

# Dropdown for minimum number of orders
min_orders = st.sidebar.selectbox("Minimum Number of Orders", options=[1, 5, 10, 20])
customer_order_counts = filtered_data.groupby('customer_id')['order_id'].nunique()
filtered_customer_ids = customer_order_counts[customer_order_counts > min_orders].index
filtered_data = filtered_data[filtered_data['customer_id'].isin(filtered_customer_ids)]

# Main Dashboard
st.title("Customer Orders Dashboard")

# Display filtered data in a table
st.subheader("Filtered Data")
st.dataframe(filtered_data)

# Summary section
st.subheader("Summary")
total_revenue = filtered_data['total_amount'].sum()
unique_customers = filtered_data['customer_id'].nunique()
total_orders = filtered_data['order_id'].nunique()

st.write("Total Revenue: $", total_revenue)
st.write("Unique Customers:", unique_customers)
st.write("Total Orders:", total_orders)

# Bar chart: Top 10 customers by total revenue
st.subheader("Top 10 Customers by Total Revenue")
top_customers = (filtered_data.groupby('customer_name')['total_amount']
                 .sum()
                 .sort_values(ascending=False)
                 .head(10))
st.bar_chart(top_customers)

# Line chart: Revenue over time (grouped by month)
st.subheader("Total Revenue Over Time")
filtered_data['order_date'] = pd.to_datetime(filtered_data['order_date'])  # Ensure it is a Timestamp for grouping
revenue_over_time = (filtered_data.resample('ME', on='order_date')['total_amount']
                     .sum())
st.line_chart(revenue_over_time)
