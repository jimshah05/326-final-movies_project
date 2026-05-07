import pandas as pd

class MovieUpdater: 
    """works with missing values in the movie file"""
    def __init__(self, file_name): 
        """sets up the file name and movie data."""
        self.file_name = file_name 
        self.movie_data = None 
       
    def extract(self):
        """reads the xlsx. file"""
        self.movie_data = pd.read_excel(self.file_name)
        return self.movie_data 
    
    def transform(self): 
        """ fills in missing values."""
        print("Missing values before updating")
        print(self.movie_data.isnull().sum())

        self.movie_data = self.movie_data.fillna("Unknown")

        print("Missing values after updating:")
        print(self.movie_data.isnull().sum()) 

        return self.movie_data 
    def load(self, new_file_name): 
        """saves the updated data as a CSV file."""

        self.movie_data.to_csv(new_file_name, index=False)
        print(f"Updated CSV file saved as {new_file_name}")


if __name__ == "__main__":

    updater = MovieUpdater("movies_2.xlsx")

    updater.extract()
    updater.transform()
    updater.load("movies_2_updated.csv")

    




    

