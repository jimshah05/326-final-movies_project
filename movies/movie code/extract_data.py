import pandas as pd
import glob as gl
import os 

class movie_extract:

    def __init__(self , movie_table):

        self.movie_table = movie_table
        self.missing_info = []


    def data_search(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        excel_file = os.path.join(dir_path , self.movie_table)

        df = pd.read_excel(excel_file)
        data = df.set_index("Movie").to_dict(orient = "index")
        # print(data)
        return data 

    def check_null(self , data):

        missing_movie_detail = {}

        for movie , m_info in data.items():


            for column , info in m_info.items():

                if pd.isna(info):

                    if movie not in missing_movie_detail:
                        missing_movie_detail[movie] = {}

                    missing_movie_detail[movie][column] = [info]
                    # print(missing_movie_detail)
                



        return missing_movie_detail
         



            














movie_extraction = movie_extract("movies_2.xlsx")
print(movie_extraction.data_search())
print(movie_extraction.check_null(movie_extraction.data_search()))

