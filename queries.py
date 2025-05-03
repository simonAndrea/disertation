import os, pyodbc, pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import urllib

# Load environment variables from .env file
load_dotenv()

# Database connection configuration
SERVER = os.getenv('DB_SERVER')
DATABASE = os.getenv('DB_NAME')
USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')

def get_engine():
    connection_string = (
        f"DRIVER={{SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes;"
    )
    params = urllib.parse.quote_plus(connection_string)
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Function to retrieve sales data for a given date range
def get_sales_data(start_date=None, end_date=None):
    query = """
    SELECT CAST(DocumentDate AS DATE) AS Date, SUM(TotalPayment) AS TotalSales
    FROM FiscalNote
    WHERE DocumentStateId <> 35
    """
    
    if start_date and end_date:
        query += f" AND DocumentDate >= '{start_date}' AND DocumentDate < '{end_date}'"
    elif start_date:
        query += f" AND DocumentDate >= '{start_date}'"
    elif end_date:
        query += f" AND DocumentDate < '{end_date}'"
        
    query += " GROUP BY CAST(DocumentDate AS DATE) ORDER BY Date;"
    
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

def getTop10Products():
    query = """
    select top 10 count(fnd.ItemId) count, i.ItemName
    from FiscalNoteDetail fnd
    inner join Item i on i.ItemId = fnd.ItemId
    where ItemName not like '%DISCOUNT%' and ItemName not like '%PUNGI%' and ItemName not like '%PUNGA%' and ItemName not like '%BON%'
    group by i.ItemName
    order by count desc
    """
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

def getSitePerformance():
    query = """select SiteId, sum(TotalPayment) as TotalAmount
    from FiscalNote
    where DocumentStateId <> 35 and SiteId in (5,6,7,8,9, 14,15)
    group by SiteId
    order by TotalAmount desc
    """
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(query, conn)
    
def getPaymentMethodsByDateAndSite(date = None):
    query = """ 
        select
            SiteId,
            sum(TotalPayment) TotalPayment, 
            sum(CashAmount) CashAmount,  
            sum(CardAmount) CardAmount, 
            sum(TicketPaymentAmount) TicketAmount
        from FiscalNote 
        where DocumentStateId <> 35 and TotalAmount >= 0 """
    
    if date:
        query += f" and DocumentDate = '{date}' group by SiteId"
    else:
        query += """ group by SiteId"""
    
    
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(query, conn)
    
def getMembership():
    query = """SELECT mct.CardTypeId, fn.TotalPayment
        FROM FiscalNote fn
        LEFT JOIN MembershipCard mc 
            ON fn.MembershipCardId = mc.MembershipCardId
        LEFT JOIN MembershipCardType mct 
            ON mc.CardTypeId = mct.CardTypeId
        WHERE 
            fn.DocumentStateId <> 35
            AND fn.TotalPayment > 0
            AND fn.DocumentDate >= (
                SELECT DATEADD(DAY, -6, MAX(DocumentDate)) 
                FROM FiscalNote
                WHERE DocumentStateId <> 35 AND TotalPayment > 0
            )
            AND (mct.CardTypeId IN (17, 24) OR fn.MembershipCardId IS NULL);
    """
    
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(query, conn)
    
def getMembershipForHistogram(id=None):
    query="""
        SELECT mct.CardTypeId, fn.TotalPayment
        FROM FiscalNote fn
        LEFT JOIN MembershipCard mc 
            ON fn.MembershipCardId = mc.MembershipCardId
        LEFT JOIN MembershipCardType mct 
            ON mc.CardTypeId = mct.CardTypeId
        WHERE 
            fn.DocumentStateId <> 35
            AND fn.TotalPayment > 0
            AND fn.DocumentDate >= (
                SELECT DATEADD(DAY, -6, MAX(DocumentDate)) 
                FROM FiscalNote
                WHERE DocumentStateId <> 35
            )  AND TotalPayment > 1
            AND """
    if id=='Employee':
        query += " mct.CardTypeId = 17"
    elif id=='Fidelity':
        query += " mct.CardTypeId = 24"
    elif id=='No Card':
        query += " fn.MembershipCardId IS NULL"
    
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

def get_forecast_data():
    query = """
    SELECT 
        CAST(DocumentDate AS DATE) AS Date,
        SUM(TotalPayment) AS Sales
    FROM FiscalNote
    WHERE 
        DocumentStateId <> 35
        AND TotalPayment > 0
    GROUP BY CAST(DocumentDate AS DATE)
    ORDER BY Date;
    """
    
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(query, conn)