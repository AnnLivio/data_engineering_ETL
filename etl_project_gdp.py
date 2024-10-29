# Code for ETL operations on Country-GDP data

# Importing the required libraries
import pandas as pd
import numpy as np 
import sqlite3
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def extract(url, table_attribs):
    ''' This function extracts the required
    information from the website and saves it to a dataframe. The
    function returns the dataframe for further processing. '''
    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, "html.parser")
    df = pd.DataFrame(columns=table_attribs)

    tables = data.find_all('tbody')
    rows = tables[2].find_all('tr')

    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            if col[0].find('a') is not None and '—' not in col[2]:
                data_dict = {"Country": col[0].a.contents[0],
                             "GDP_USD_millions": col[2].contents[0]}
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df,df1], ignore_index=True)
    return df

def transform(df):
    ''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP from
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.'''
    GDP_list = df["GDP_USD_millions"].tolist()
    GDP_list = [float("".join(x.split(','))) for x in GDP_list]
    GDP_list = [np.round(x/1000,2) for x in GDP_list]
    df["GDP_USD_millions"] = GDP_list
    df=df.rename(columns = {"GDP_USD_millions":"GDP_USD_billions"})

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


def log_progress(message):
    ''' This function logs the mentioned message at a given stage of the code execution to a log file. 
    Function returns nothing'''
    timestamp_format = '%Y-%h-%d-%H:%M:%S' #Year-Month-Day Hour:Minutes:Seconds
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open("./etl_project_log.txt", "a") as f:
        f.write(timestamp + ',' + message + '\n')


''' Here, you define the required entities and call the relevant 
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''

# Log the initialization of the ETL process 
log_progress("ETL Job Started") 

# Declaring variables required
log_progress("Preliminaries complete. Initiating ETL process.")
url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
table_attribs = ['Country', 'GDP_USD_millions']
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
csv_path = './countries_by_gdp.csv'


# Call extract() function 
log_progress("Data extraction complete. Initiating Transformation process.") 
df = extract(url, table_attribs)
 
 
# Call transform() function
log_progress("Data transformation complete. Initiating loading process.") 
transformed_df = transform(df) 
print("Transformed Data") 
print(transformed_df) 
 
# Call load_to_csv() 
log_progress("Data saved to CSV file.") 
load_to_csv(transformed_df, csv_path)
 

# Initiate SQLite3 connection
log_progress("SQL Connection initiated.") 
conn = sqlite3.connect(db_name)

# Call load_to_db()
log_progress("Data loaded to Database as table. Running the query.")
load_to_db(transformed_df, conn, table_name)

# Call run_query()
log_progress("Process Complete")
query_statement = f"SELECT * FROM {table_name} WHERE GDP_USD_billions >= 100"
run_query(query_statement, conn)

# Close SQLite3 connection
conn.close() 