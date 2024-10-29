import sqlite3
import pandas as pd

# Create a connection to a new db "STAFF"
conn = sqlite3.connect("STAFF.db")

table_name = 'INSTRUCTOR'
attribute_list = ['ID', 'FNAME', 'LNAME', 'CITY', 'CCODE']

# Read the csv file
file_path = '/home/project/INSTRUCTOR.csv'
df = pd.read_csv(file_path, names = attribute_list)

# Load data to the table
df.to_sql(table_name, conn, if_exists = 'replace', index=False)
print("Table is ready")

def make_query(query_statement):
    query_output = pd.read_sql(query_statement, conn)
    print(query_statement)
    print(query_output)

query_statement = f"SELECT * FROM {table_name}"
make_query(query_statement)


# View onle FNAME column
query_statement = f"SELECT FNAME FROM {table_name}"
make_query(query_statement)

# View the total number of entries in the table
query_statement = f"SELECT COUNT(1) FROM {table_name}"
make_query(query_statement)

# Append data to the table
data_dict = {'ID': [100],
            'FNAME': ['Jane'],
            'LNAME': ['Doe'], 
            'CITY': ['Paris'], 
            'CCODE':['FR']}
data_append = pd.DataFrame(data_dict)
data_append.to_sql(table_name, conn, if_exists='append', index=False)
print('Data appended successfuly')

# Repeat the count  of total number of entries in the table
query_statement = f"SELECT COUNT(1) FROM {table_name}"
make_query(query_statement)

conn.close()