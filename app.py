import os, pyodbc, pandas as pd, streamlit as st, matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection configuration
SERVER = os.getenv('DB_SERVER')
DATABASE = os.getenv('DB_NAME')
USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')

conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;')

table = 'FiscalNote'

# Fetch data from MSSQL
query = "SELECT TOP 10 * FROM {table}"
query = query.format(table=table)
data = pd.read_sql(query, conn)

# Streamlit App Title
st.title('Data Visualizations')

# Display the raw data in the Streamlit app
st.write("### Data Preview", data.head())

# Create a simple plot using Matplotlib or Plotly
st.write("### Plot Example")

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(data.index, data['TotalAmount'], label='DocumentDate', color='tab:blue')
ax.set(title=f"Line Chart for {'TotalAmount'}", xlabel="Date", ylabel="Value")
ax.legend()

st.pyplot(fig)