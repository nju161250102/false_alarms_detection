import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from .DataLoader import DataLoader


class OneHotDataLoader(DataLoader):

    def __init__(self, data_dir: str):
        super().__init__(data_dir)

    def read_data(self, len_limit: int):
        text_data = []
        id_list = []
        for file_path, file_label in self.file_list:
            df = pd.read_csv(file_path, header=None)
            text_data.append(" ".join([str(s) for s in df.values.tolist()[0]]))
            id_list.append(file_label)
        encoder = OneHotEncoder()
        all_text = " ".join(text_data).split(" ")
        encoder.fit(np.array(all_text).reshape(len(all_text), -1))
        for i in range(len(text_data)):
            text_list = text_data[i].split(" ")
            one_text = encoder.transform(np.array(text_list).reshape(len(text_list), - 1)).toarray().tolist()
            if len(one_text) > len_limit:
                one_text = one_text[:len_limit]
            else:
                for k in range(len(one_text), len_limit):
                    one_text.append([0 for j in range(len(one_text[0]))])
            self.data_list.append((one_text, id_list[i]))
