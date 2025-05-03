library(odbc)
library(dotenv)

# Load environment variables
load_dot_env()

# Create database connection
con <- dbConnect(odbc(),
    Driver = "SQL Server",
    Server = Sys.getenv("DB_SERVER"),
    Database = Sys.getenv("DB_NAME"),
    UID = Sys.getenv("DB_USER"),
    PWD = Sys.getenv("DB_PASSWORD")
)

# Example query
data <- dbGetQuery(con, "SELECT 
    CAST(DocumentDate AS DATE) AS Date, 
    SUM(TotalPayment) AS TotalSales
    FROM FiscalNote
    WHERE DocumentStateId <> 35
    GROUP BY CAST(DocumentDate AS DATE)")

# Close connection when done
dbDisconnect(con)