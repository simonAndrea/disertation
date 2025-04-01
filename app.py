from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
import pyodbc
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Database connection configuration
SERVER = os.getenv('DB_SERVER')
DATABASE = os.getenv('DB_NAME')
USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')

def get_db_connection():
    conn_str = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'
    return pyodbc.connect(conn_str)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data/<table_name>')
def get_top_10(table_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = f"SELECT TOP 10 * FROM {'FiscalNote'}"
        cursor.execute(query)
        
        columns = [column[0] for column in cursor.description]
        rows = []
        for row in cursor.fetchall():
            rows.append(dict(zip(columns, row)))
        
        conn.close()
        return jsonify({'data': rows, 'columns': columns, 'table_name': table_name})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)