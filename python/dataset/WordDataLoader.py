import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from .DataLoader import DataLoader


class WordDataLoader(DataLoader):

    def __init__(self, data_dir: str):
        super().__init__(data_dir)

    def read_data(self, handler: str):
        text_data = []
        id_list = []
        for file_path, file_label in self.file_list:
            df = pd.read_csv(file_path, header=None)
            text_data.append(" ".join([str(s) for s in df.values.tolist()[0]]))
            id_list.append(file_label)
        vectorizer = CountVectorizer() if handler == "Count" else TfidfVectorizer()
        vector_array = vectorizer.fit_transform(text_data).toarray()
        for i in range(len(vector_array)):
            self.data_list.append((vector_array[i], id_list[i]))
