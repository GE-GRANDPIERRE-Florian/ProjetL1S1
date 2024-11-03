import os, csv
import time

class Langue:
    def __init__(self, file_path) -> None:
        self.__data : dict = {}
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                reader = csv.DictReader(f, delimiter=";")
                for row in reader:
                    key : str = row["Id"]
                    self.__data[key] = row["Text"]
        else:
            raise FileNotFoundError("File does not exist")
        
    def get_text(self, text_id: str) -> str:
        if text_id in self.__data: return self.__data[text_id]
        else: return text_id

languages_aivalable : dict = {
    "fr_FR": Langue("./Ressources/Languages/fr_FR.csv"),
    "en_EN": Langue("./Ressources/Languages/en_EN.csv")
}