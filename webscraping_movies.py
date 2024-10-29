import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies.db'
table_name = 'Top_50'
csv_path = '/home/project/top_50_films.csv'
df = pd.DataFrame(columns=['Average Rank', 'Film', 'Year'])
count = 0

# Load the webpage for Wescraping
html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

# Scraping of required information
# tables gets the body of all the tables in the web page 
tables = data.find_all('tbody')

# rows gets all the rows of the first table.
rows = tables[0].find_all('tr')

# Iterate over the rows to find required data
for row in rows:
    # Check for the loop counter to restrict to 50 entries.
    if count < 50:
        # Extract all the td data objects in the row 
        col = row.find_all('td')
        if len(col) != 0:
            data_dict = {"Average Rank": int(col[0].contents[0]),
                        "Film": str(col[1].contents[0]),
                        "Year": int(col[2].contents[0])}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df, df1], ignore_index=True)
            # Increment the loop counter
            count += 1
    else:
        break
    
print(df)
df.to_csv(csv_path)

# Initialize a connection to the database to store the data in a db 
conn = sqlite3.connect(db_name)

# Save the dataframe as a table
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Close the connection.
conn.close()

