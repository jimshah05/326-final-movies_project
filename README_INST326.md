
# Final Project INST326
 


## Overview
This project was built as a final project for INST326. It takes a movie dataset in Excel format, detects rows with missing values, and uses web scraping (we're using Selenium) to fetch the missing data from the IMDb website. It can also look up any movie by title or IMDb ID on demand.
## Features
- Reads movie data from an Excel file
- Detects missing values across all columns
- Scrapes IMDb to fill in missing values such as:
    - Runtime
    - IMDb Rating
    - Release Date
    - Genre
    - Director
- Saves the cleaned dataset to a new CSV file
-Lets users search for any movie by title or IMDb ID and retreieve full details
## How Its Works
The project is structured as an ETL (Extract, Transform, Load) pipeline using three classes:

    1. move_extract -- Extract
    Reads the Excel file and builds a dictionary of all movie data. A second pass 
    identifies only the rows with missing values, flagging them for scraping. 

    2. Transform -- Transform
    Takes the dictionary of movies with missing data and launches a Selenium 
    controlled Chrome browser. It navigates to each movie's IMDb page (using the IMDb ID 
    to avoid duplicate title issues) and scrapes the missing fields. A seperate method, get_user_movie(), lets 
    users input a movie title or IMDb ID to retrieve full movie details on demand. 

    3. MovieUpdater -- Load
    Reads the original Excel file again, fills in the scraped values, and 
    exports the final results as a cleaned CSV file. 


## Requirements
- Python
- Google Chrome + matching ChromeDriver
- The following Python packages:
    - pandas
    - openpyxl
    - selenium

## Install these 3 by doing  
    pip install pandas openpyxl selenium

## Run the full pipeline
    python final_project.py 

This will:
- Read movies_2.xlsx
- Detect all missing values
- Scrape IMDb for the missing data
- Save the cleaned output to movies_2_updated.csv

## Look up a specific movie  
Inside final_project.py, call:  

    transform.get_user_movie("Inception") # by title  
    transform.get_user_movie("tt1375666") # by IMDb ID
