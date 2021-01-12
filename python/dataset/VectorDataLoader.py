import pandas as pd
from .DataLoader import DataLoader


class VectorDataLoader(DataLoader):

    def __init__(self, data_dir: str):
        super().__init__(data_dir)

    def read_data(self, len_limit: int):
        for file_path, file_label in self.file_list:
            df = pd.read_csv(file_path, header=None)
            feature_len = df.shape[0]
            x_data = []
            for index, row in df.iterrows():
                if index < len_limit:
                    x_data.append(list(row))
            if feature_len < len_limit:
                for i in range(feature_len, len_limit):
                    x_data.append([0 for j in range(df.shape[1])])
            self.data_list.append((x_data, file_label))
