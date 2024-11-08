
# Data Engineering and Analysis Solution

## Objective
The objective of this project is to design and implement a data engineering solution that:
1. Imports customer and order data from CSV files into a MySQL database.
2. Analyzes the data using a Streamlit web application.

The project consists of three main parts:
- **Part 1: Data Preparation**
- **Part 2: Streamlit App Setup**
- **Part 3: Data Analysis (Bonus)**

## Project Overview
This solution involves the following tasks:
- Importing customer and order data from CSV files into a MySQL database using SQLAlchemy.
- Creating a Streamlit web application to allow users to interact with the data and visualize key metrics.
- (Bonus) Implementing a simple machine learning model to predict repeat customers.

## Requirements
Before running the project, make sure you have the following dependencies installed:

```bash
pip install pandas sqlalchemy mysql-connector-python streamlit scikit-learn
```

Additionally, ensure that you have:
- MySQL installed and configured on your machine.
- A database named `mydb` (or modify the connection settings as needed).

## Part 1: Data Preparation

### 1. Data Import
The first part of the project is to import customer and order data from the provided CSV files (`customers.csv` and `orders.csv`) into a MySQL database. The database schema consists of two tables:
- **Customers Table**: Contains `customer_id` and `customer_name`.
- **Orders Table**: Contains `order_id`, `customer_id`, `total_amount`, and `order_date`.

The Python script used to import the data can be found in the `data_import.py` file. It uses `SQLAlchemy` to connect to the MySQL database and load the data from the CSV files into the respective tables.

### 2. Database Connection
The connection to the MySQL database is managed securely using SQLAlchemy. Below is an overview of how the connection is established:

```python
from sqlalchemy import create_engine

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
```

Ensure that your MySQL credentials are correctly set up in the `db_config` dictionary.

## Part 2: Streamlit App Setup

### 1. Sidebar Filters
The Streamlit application allows users to filter data with the following components:
- **Date Range Filter**: Filters orders by `order_date`.
- **Slider**: Filters customers who have spent more than a specified amount (e.g., more than $1000).
- **Dropdown**: Filters customers who have made more than a specified number of orders (e.g., more than 5 orders).

The filter setup in the sidebar is as follows:

```python
# Date range filter
start_date, end_date = st.sidebar.date_input("Select Order Date Range", [dt.date(2023, 1, 1), dt.date.today()])

# Slider for total amount spent
min_total_amount = st.sidebar.slider("Minimum Total Amount Spent", 0, 5000, 1000)

# Dropdown for minimum number of orders
min_orders = st.sidebar.selectbox("Minimum Number of Orders", options=[1, 5, 10, 20])
```

### 2. Main Dashboard
The main dashboard displays key insights, including:
- **Filtered Data**: Displays the filtered customer and order data in a table.
- **Bar Chart**: Shows the top 10 customers by total revenue.
- **Line Chart**: Displays the total revenue over time (grouped by week/month).
- **Summary Section**: Displays key metrics such as total revenue, the number of unique customers, and the total number of orders.

Here is how the data is displayed and analyzed:

```python
# Display filtered data in a table
st.subheader("Filtered Data")
st.dataframe(filtered_data)

# Summary section
total_revenue = filtered_data['total_amount'].sum()
unique_customers = filtered_data['customer_id'].nunique()
total_orders = filtered_data['order_id'].nunique()

st.write("Total Revenue: $", total_revenue)
st.write("Unique Customers:", unique_customers)
st.write("Total Orders:", total_orders)
```

## Part 3: Data Analysis

### 1. Machine Learning Model
As a bonus task, a simple machine learning model (Logistic Regression) has been implemented to predict whether a customer is a repeat purchaser. The model uses the following features:
- Total number of orders (`total_orders`).
- Total revenue (`total_revenue`).

Here is the code to train the model:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# Feature engineering: Creating 'is_repeat_customer' column
customer_data['is_repeat_customer'] = (customer_data['total_orders'] > 1).astype(int)

# Define features (X) and target (y)
X = customer_data[['total_orders', 'total_revenue']]
y = customer_data['is_repeat_customer']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions and evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy}")
```

This code trains the model and evaluates its accuracy.

## Running the Project

To run the project, follow these steps:
1. Make sure the MySQL database is set up and running.
2. Import the data from CSV into the database by running the `Delivergate1.ipynb` script.
3. Launch the Streamlit app using the following command:

```bash
streamlit run app.py
```


