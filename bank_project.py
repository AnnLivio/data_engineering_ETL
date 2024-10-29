# Code for ETL operations on Banks data

# Importing the required libraries
import pandas as pd
import numpy as np 
import sqlite3
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Log function
def log_progress(message):
    ''' Logs the message at a given stage of the code execution to a log file.'''
    timestamp_format = '%Y-%h-%d-%H:%M:%S' #Year-Month-Day Hour:Minutes:Seconds
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open("./code_log.txt", "a") as f:
        f.write(timestamp + ',' + message + '\n')

def extract(url, table_attribs):
    ''' Extracts the required information from the website and saves it to a dataframe. 
    The function returns the dataframe for further processing. '''
    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, "html.parser")
    df = pd.DataFrame(columns=table_attribs)

    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')

    for row in rows:
        col = row.find_all("td")
        if len(col) != 0:
            data_dict = {"Name": col[1].find_all("a")[1]["title"],
                         "MC_USD_Billion": float(col[2].contents[0][:-1])}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df, df1], ignore_index=True)

    return df  


def transform(df):
    ''' This function create the columns  MC_GBP_Billion, MC_EUR_Billion, MC_INR_Billion.
    The function returns the transformed dataframe.'''
    # Read exchange rate CSV file
    exchange_rate = pd.read_csv("./exchange_rate.csv")

    # Convert to a dictionary with "Currency" as keys and "Rate" as values
    exchange_rate = exchange_rate.set_index("Currency").to_dict()["Rate"]

    # Add MC_GBP_Billion, MC_EUR_Billion, and MC_INR_Billion
    # columns to dataframe. Round off to two decimals
    df["MC_GBP_Billion"] = np.round(df["MC_USD_Billion"] * exchange_rate["GBP"], 2)
    df["MC_EUR_Billion"] = np.round(df["MC_USD_Billion"] * exchange_rate["EUR"], 2)
    df["MC_INR_Billion"] = np.round(df["MC_USD_Billion"] * exchange_rate["INR"], 2)

    return df


def load_to_csv(df, csv_path):
    ''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''
    df.to_csv(csv_path)


def load_to_db(df, sql_connection, table_name):
    ''' Save the final dataframe as a database table
    with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)


def run_query(query_statement, sql_connection):
    ''' Run the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_statement)
    print(query_output)



# Log the initialization of the ETL process 
log_progress("ETL Job Started") 

# Declaring variables required
log_progress("Preliminaries complete. Initiating ETL process.")
url = "https://web.archive.org/web/20230908091635%20/https://en.wikipedia.org/wiki/List_of_largest_banks"
table_attribs = ['Name', 'MC_USD_Billion'] # Name, MC_USD_Billion, MC_GBP_Billion, MC_EUR_Billion, MC_INR_Billion
db_name = 'Banks.db'
table_name = 'Largest_banks'
csv_path = './Largest_banks_data.csv'


# Call extract() function 
log_progress("Data extraction complete. Initiating Transformation process.") 
df = extract(url, table_attribs)
print(df) 
 
# Call transform() function
log_progress("Data transformation complete. Initiating loading process.") 
df = transform(df)
 
# Call load_to_csv() 
log_progress("Data saved to CSV file.") 
load_to_csv(df, csv_path)

# Initiate SQLite3 connection
log_progress("SQL Connection initiated.") 
conn = sqlite3.connect(db_name)

# Call load_to_db()
log_progress("Data loaded to Database as table. Running the query.")
load_to_db(df, conn, table_name)


# Call run_query()
# View content of the table
query_statement = f"SELECT * FROM {table_name}"
run_query(query_statement, conn)

# AVG market capitalization of all banks
query_statement = f"SELECT AVG(MC_GBP_Billion) FROM {table_name}"
run_query(query_statement, conn)

# Name of the top 5 banks
query_statement = f"SELECT Name FROM {table_name} LIMIT 5"
run_query(query_statement, conn)

# Close SQLite3 connection
conn.close() 
