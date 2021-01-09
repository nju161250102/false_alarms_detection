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
        # One-Hot 编码
        if handler == "OneHot":
            encoder = OneHotEncoder()
            all_text = " ".join(text_data).split(" ")
            encoder.fit(np.array(all_text).reshape(len(all_text), -1))
            for i in range(len(text_data)):
                text_list = text_data[i].split(" ")
                self.data_list.append((encoder.transform(np.array(text_list).reshape(len(text_list), - 1)), id_list[i]))
            return
        # 词频编码或TD-IDF编码
        else:
            vectorizer = CountVectorizer() if handler == "Count" else TfidfVectorizer()
            vector_array = vectorizer.fit_transform(text_data).toarray()
            for i in range(len(vector_array)):
                self.data_list.append((vector_array[i], id_list[i]))
