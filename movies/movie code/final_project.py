from selenium import webdriver 
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os 
import re
from datetime import datetime


class movie_extract:

    def __init__(self , movie_table):

        self.movie_table = movie_table
        self.missing_info = []
        self.missing_movie_detail = {}


    def data_search(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        excel_file = os.path.join(dir_path , self.movie_table)

        df = pd.read_excel(excel_file)
        df["Date"] = pd.to_datetime(df["Date"] ,  errors="coerce").dt.strftime(" %Y ,%m ,%d")
        data = df.set_index("Movie").to_dict(orient = "index")
        # print(data)
        return data 

    def check_null(self , data):

        for movie , m_info in data.items():


            for column , info in m_info.items():

                if pd.isna(info):

                    if movie not in self.missing_movie_detail:
                        self.missing_movie_detail[movie] = {'IMDB_ID' : m_info['IMDB_ID']}

                    self.missing_movie_detail[movie][column] = info
                    # print(missing_movie_detail)
                

        print(self.missing_movie_detail)

        return self.missing_movie_detail
         




class Transform:


    def __init__(self , extracted_data):

        self.extracted_data = extracted_data
        self.found_info = {}
    
    def web_search(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        chrome_driver_path = os.path.join(current_path , "chromedriver.exe")

                # print(f"This is the {movie} and this is the info {info}")
        service = Service(executable_path=chrome_driver_path)
                # this tells python to use this chromedriver to control and run chrome 

        driver = webdriver.Chrome(service=service)
                # this launches the chrome browser that selenium can control 

        driver.get("https://www.imdb.com")
                # this gets the website which we would be using 

        wait = WebDriverWait(driver ,5)
                # this tells the program to wait 10 secs on driver 


        for movie , column in self.extracted_data.missing_movie_detail.items():
            movie = str(movie)
            imdb_id = column['IMDB_ID'] 

            current_url = driver.current_url
            driver.get(f"https://www.imdb.com/title/{imdb_id}/")
            time.sleep(3)



           
            

            if 'Length' in column and pd.isna(column.get('Length')):
                all_results = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ipc-inline-list__item"))) 

                for info in all_results:

                    modified_text = info.text.strip()

                    if re.match(r'^\d+h(\s\d+m)?$|^\d+m$', modified_text):
                       self.found_info['Length'] = modified_text 
                       print(f" {movie} and - {self.found_info}")
                       break
           
            elif 'Rating' in column and pd.isna(column.get('Rating')):
                all_results = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="hero-rating-bar__aggregate-rating__score"]'))) 
                modified_text = all_results.get_attribute("innerText").strip()

                if re.search(r'(\d+(?:\.\d+)?)', modified_text):

                    self.found_info["Rating"] = modified_text
                    print(f" {movie} and - {self.found_info}")
    
    def get_user_movie(self , user_movie):

        driver = webdriver.Chrome()
        

        if re.match(r"^tt\d{7,8}$" , user_movie):

            driver.get(f"https://www.imdb.com/title/{user_movie}/")
            time.sleep(3)

        else:
            driver.get("https://www.imdb.com")
            wait = WebDriverWait(driver , 5)
            all_results = wait.until(EC.presence_of_element_located((By.ID, "suggestion-search"))) 

            all_results.send_keys(user_movie)
            all_results.send_keys(Keys.ENTER)
            first_search_result = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li a[href^='/title/tt']")))
            first_search_result.click()
            time.sleep(4)

        finding_length_user = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ipc-inline-list__item"))) 
        finding_rating_user = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="hero-rating-bar__aggregate-rating__score"]'))) 
        finding_date_user = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ipc-metadata-list__item"))) 
        finding_genre_user = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ipc-chip-list__scroller"))) 
        for info in finding_length_user:

                    modified_text = info.text.strip()

                    if re.match(r'^\d+h(\s\d+m)?$|^\d+m$', modified_text):
                       self.found_info['Length'] = modified_text 
                    #    print(f" {user_movie} - {self.found_info}")
                       break
        modified_text = finding_rating_user.get_attribute("innerText").strip()
        if re.search(r'(\d+(?:\.\d+)?)', modified_text):

                    self.found_info["Rating"] = modified_text
                    # print(f" {user_movie} and - {self.found_info}")
        
        for the_info in finding_date_user:
             modified_text = the_info.get_attribute("innerText").strip()

             if re.search(r"United States" , modified_text):
                   date_match = re.search(r"[A-Z][a-z]+ \d{1,2}, \d{4}", modified_text)
                   if date_match:
                        date_text = date_match.group()

                        date_object = datetime.strptime(date_text, "%B %d, %Y")
                        formatted_date = date_object.strftime(" %Y ,%m ,%d")

                        self.found_info["Date"] = formatted_date
                        print(f"{user_movie} and - {self.found_info}") 
        modified_text = finding_genre_user.get_attribute("innerText").strip('\n')
        genres = modified_text.split("\n")
    
        # genre_match = re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)?(?:\s[A-Za-z]+(?:-[A-Za-z]+)?)*", modified_text)

        if genres:
             self.found_info["Genre"] = " , " .join(genres)
             print(self.found_info)
                       
        


        
        

        

            
  








movie_extraction = movie_extract("movies_2.xlsx")

data = movie_extraction.data_search()

movie_extraction.check_null(data)

transform = Transform(movie_extraction)

transform.get_user_movie('Spider-Man')





  
