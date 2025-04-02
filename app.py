import os
from dotenv import load_dotenv
import pyodbc
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Database connection configuration
SERVER = os.getenv('DB_SERVER')
DATABASE = os.getenv('DB_NAME')
USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')

conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;')

# Fetch data from MSSQL
query = "SELECT TOP 10 * FROM FiscalNote"
data = pd.read_sql(query, conn)

# Show the data
print(data.head())