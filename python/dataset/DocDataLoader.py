import pandas as pd
from .DataLoader import DataLoader


class DocDataLoader(DataLoader):

    def __init__(self, data_dir: str):
        super().__init__(data_dir)

    def read_data(self):
        for file_path, file_label in self.file_list:
            df = pd.read_csv(file_path, header=None)
            self.data_list.append((df.values.tolist()[0], file_label))
