import os
import pandas as pd
import json
import base64

class DataLoader(object):
    def __init__(self, data_csv, image_folder):
        self.data_csv = data_csv
        self.image_folder = image_folder
        self.data = pd.read_csv(data_csv)
        self.data.drop(['Unnamed: 0'], axis=1, inplace=True)

    def get_data(self, index):
        index = int(index)
        entry = dict(self.data.loc[index])
        with open(os.path.join(self.image_folder, entry['image_path']), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        entry['image_data'] = 'data:image/jpg;base64,' + encoded_string.decode('utf-8')
        return entry
