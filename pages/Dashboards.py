import os, pyodbc, pandas as pd, streamlit as st, matplotlib.pyplot as plt
from dotenv import load_dotenv


st.set_page_config(
    page_title="OptiView",
    page_icon=":chart_with_upwards_trend:",
)

#Using CSS file
with open('main_style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title(":bar_chart: Visualization Dashboards")

# Load environment variables from .env file
load_dotenv()

# Database connection configuration
SERVER = os.getenv('DB_SERVER')
DATABASE = os.getenv('DB_NAME')
USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')

conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;')

# Fetch data from MSSQL
query = "SELECT CAST(DocumentDate AS DATE) AS Date, SUM(TotalAmount) AS TotalSales FROM FiscalNote WHERE DocumentStateId <> 35 GROUP BY CAST(DocumentDate AS DATE) ORDER BY Date;"
totalAmounts = pd.read_sql(query, conn)

# Streamlit App Title
st.title('Data Visualizations')

st.subheader('Total Sales Over Time')

st.line_chart(totalAmounts.set_index('Date')['TotalSales'])