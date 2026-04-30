from selenium import webdriver 
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os 



class movie_extract:

    def __init__(self , movie_table):

        self.movie_table = movie_table
        self.missing_info = []
        self.missing_movie_detail = {}


    def data_search(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        excel_file = os.path.join(dir_path , self.movie_table)

        df = pd.read_excel(excel_file)
        data = df.set_index("Movie").to_dict(orient = "index")
        # print(data)
        return data 

    def check_null(self , data):


        for movie , m_info in data.items():


            for column , info in m_info.items():

                if pd.isna(info):

                    if movie not in self.missing_movie_detail:
                        self.missing_movie_detail[movie] = {}

                    self.missing_movie_detail[movie][column] = [info]
                    # print(missing_movie_detail)
                



        return self.missing_movie_detail
         




class Transform:


    def __init__(self , extracted_data):

        self.extracted_data = extracted_data

    
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
            for column_name , info in column.items():

                
                input_element = wait.until(EC.presence_of_element_located((By.ID , "suggestion-search")))
                # # this waits until the search bar with ID "suggestion-search" appears on the page then saves that search bar in input_element

                input_element.send_keys(str(movie) + Keys.ENTER)
                # # this enters monkey or wtv movie you want in the search bar and than clicks the enter button 

                time.sleep(15)

                # stays on that chrome or google screen for that long than quits 
                all_results = wait.until(
                        EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"[data-testid='find-results-section-title'] a"))
                    )

                found = False
                for result in all_results:
                        if movie in result.text:
                            found = True
                            break

                if found:
                            
                            if len(all_results) > 0:
                                 print(f"IMDb found something for {movie}: {all_results[0].text}")
                            
                else:
                            print("oopsy doozy")





movie_extraction = movie_extract("movies_2.xlsx")

data = movie_extraction.data_search()

movie_extraction.check_null(data)

transform = Transform(movie_extraction)

transform.web_search()





  

# service = Service(executable_path="chromedriver.exe")
# # this tells python to use this chromedriver to control and run chrome 

# driver = webdriver.Chrome(service=service)
# # this launches the chrome browser that selenium can control 

# driver.get("https://www.imdb.com")
# # this gets the website which we would be using 

# wait = WebDriverWait(driver ,10)
# # this tells the program to wait 10 secs on driver 

# input_element = wait.until(EC.presence_of_element_located((By.ID , "suggestion-search")))
# # this waits until the search bar with ID "suggestion-search" appears on the page then saves that search bar in input_element

# input_element.send_keys("monkey" + Keys.ENTER)
# # this enters monkey or wtv movie you want in the search bar and than clicks the enter button 

# time.sleep(10)

# # stays on that chrome or google screen for that long than quits 



# driver.get("https://www.themoviedb.org/")

# wait = WebDriverWait(driver ,10)

# input_element = wait.until(EC.presence_of_element_located((By.ID , "search_v4")))

# input_element.send_keys("Hoppers" + Keys.ENTER)

 

# all_results = wait.until(
#     EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search_results h2 span"))
# )

# found = False
# for result in all_results:
#     if "Hip Hoppers" in result.text:
#         found = True
#         break

# if found:
#     print("woozy")
# else:
#     print("oopsy doozy")