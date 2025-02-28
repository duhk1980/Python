import logging
import azure.functions as func
import pandas as pd
import pyodbc
import os

app = func.FunctionApp()

@app.function_name(name="mytimer")
@app.timer_trigger(schedule="0 */1 * * * *", 
              arg_name="mytimer",
              run_on_startup=True) 
def test_function(mytimer: func.TimerRequest) -> None:
    try:
        # Read file path from environment
        blob_file_path = os.getenv('CsvfilePath')
        if blob_file_path is None:
            raise ValueError("CsvfilePath is not set in the environment variables.")
        
        # Read the CSV file,Using pandas into a DataFrame.
        df = pd.read_csv(blob_file_path)
        

        # Validate and Transform the DataFrame
        df.dropna(subset=['ProductID', 'ProductName', 'Category', 'Price', 'Stock'], inplace=True)
        
        df['ProductID'] = pd.to_numeric(df['ProductID'], errors='coerce').dropna().astype(int)
        df.drop_duplicates(subset=['ProductID'], inplace=True)
        
        df['ProductName'] = df['ProductName'].astype(str).str.strip()
        df['Category'] = df['Category'].astype(str).str.strip()
        
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        df = df[df['Price'] > 0]  # Ensure Price is positive
        
        df['Stock'] = pd.to_numeric(df['Stock'], errors='coerce').dropna().astype(int)
        df = df[df['Stock'] >= 0]  # Ensure Stock is non-negative

        # SQL Server Express connection using Windows Authentication
        server = 'localhost\\SQLEXPRESS'  # Update with your SQL Server Express instance name
        database = 'RetailDB'
        driver = '{ODBC Driver 17 for SQL Server}'

        conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
        cursor = conn.cursor()

        # Insert Data into SQL Database ProductCatalog Table
        for index, row in df.iterrows():
            cursor.execute("""
                INSERT INTO ProductCatalog (ProductID, ProductName, Category, Price, Stock)
                VALUES (?, ?, ?, ?, ?)
            """, row['ProductID'], row['ProductName'], row['Category'], row['Price'], row['Stock'])

        conn.commit()
        cursor.close()
        conn.close()
        logging.info('CSV data validated, transformed, and inserted into SQL database.')

    except Exception as e:
        logging.error(f"An error occurred: {e}")
