# Extract, Transform, and Load Data using Python (etl_code.py)

## Introduction
Extract, Transform and Load (ETL) operations are of extreme importance in the role of a Data engineer. A data engineer extracts data from multiple sources and different file formats, transforms the extracted data to predefined settings and then loads the data to a database for further processing. In this lab, you will get hands-on practice of performing these operations.

## Objectives
After completing this lab, you will be able to:

+ Read CSV, JSON, and XML file types.
+ Extract the required data from the different file types.
+ Transform data to the required format.
+ Save the transformed data in a ready-to-load format, which can be loaded into an RDBMS.

## Importing Libraries and setting paths
We will extract data from CSV, JSON, and XML formats. 

The xml library can be used to parse the information from an .xml file format. The .csv and .json file formats can be read using the pandas library. We will use the pandas library to create a data frame format that will store the extracted data from any file.

To call the correct function for data extraction, we need to access the file format information. For this access, we can use the glob library.

To log the information correctly, we need the date and time information at the point of logging. For this information, we require the datetime package.

While glob, xml, and datetime are inbuilt features of Python, we need to install the pandas library to our IDE.

Note that we import only the ElementTree function from the xml.etree library because we require that function to parse the data from an XML file format.

# Web scraping and Extracting Data using APIs (webscraping_movies.py)
Web scraping is used for extraction of relevant data from web pages. If we require some data from a web page in a public domain, web scraping makes the process of data extraction quite convenient. The use of web scraping, however, requires some basic knowledge of the structure of HTML pages. 

## Objectives
+ Use the requests and BeautifulSoup libraries to extract the contents of a web page
+ Analyze the HTML code of a webpage to find the relevant information
+ Extract the relevant information and save it in the required form

## Scenario
We have been hired by a Multiplex management organization to extract the information of the top 50 movies with the best average rating from the web link shared below.
[https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films]
The information required is Average Rank, Film, and Year.
We are required to write a Python script webscraping_movies.py that extracts the information and saves it to a CSV file top_50_films.csv. We are also required to save the same information to a database Movies.db under the table name Top_50.

# Accessing Databases using Python Script (db_code.py)
## Objectives
+ Create a database using Python
+ Load the data from a CSV file as a table to the database
+ Run basic "queries" on the database to access the information

## Scenario
Consider a dataset of employee records that is available with an HR team in a CSV file. As a Data Engineer, we are required to create the database called STAFF and load the contents of the CSV file as a table called INSTRUCTORS. The headers of the available data are :

|Header|	Description|
|---|---|
|ID|Employee ID|
|FNAME|	First Name|
|LNAME|Last Name|
|CITY|City of residence|
|CCODE|Country code (2 letters)|

