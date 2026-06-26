import os
import urllib
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load các biến từ file .env
load_dotenv()

def get_engine():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER")
    
    params = urllib.parse.quote_plus(
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
    )
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
