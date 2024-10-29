# Extract, Transform, and Load Data using Python

## Introduction
Extract, Transform and Load (ETL) operations are of extreme importance in the role of a Data engineer. A data engineer extracts data from multiple sources and different file formats, transforms the extracted data to predefined settings and then loads the data to a database for further processing. In this lab, you will get hands-on practice of performing these operations.

## Objectives
After completing this lab, you will be able to:

+ Read CSV, JSON, and XML file types.
+ Extract the required data from the different file types.
+ Transform data to the required format.
+ Save the transformed data in a ready-to-load format, which can be loaded into an RDBMS.

[wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Lab%20-%20Extract%20Transform%20Load/data/source.zip]

## Importing Libraries and setting paths
We will extract data from CSV, JSON, and XML formats. 

The xml library can be used to parse the information from an .xml file format. The .csv and .json file formats can be read using the pandas library. We will use the pandas library to create a data frame format that will store the extracted data from any file.

To call the correct function for data extraction, we need to access the file format information. For this access, we can use the glob library.

To log the information correctly, we need the date and time information at the point of logging. For this information, we require the datetime package.

While glob, xml, and datetime are inbuilt features of Python, we need to install the pandas library to your IDE.

Note that we import only the ElementTree function from the xml.etree library because we require that function to parse the data from an XML file format.
