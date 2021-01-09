from .DataLoader import DataLoader


class MeasureDataLoader(DataLoader):

    def __init__(self, data_dir: str):
        super().__init__(data_dir)

    def read_data(self):
        for file_path, file_label in self.file_list:
            with open(file_path) as txt_file:
                self.data_list.append(([int(s) for s in txt_file.readline().split()[:5]], file_label))
