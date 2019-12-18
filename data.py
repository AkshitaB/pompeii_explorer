import os
import pandas as pd
import json
import base64
import numpy as np
import datetime
import glob
import shutil
import chunk_align

class DataLoader(object):
    def __init__(self, data_csv, image_folder, ocr_text):
        self.data_csv = data_csv
        self.image_folder = image_folder
        self.ocr_text = ocr_text
        self.load()
        #self.data['aligned'] = "no"

    def get_data(self, index):
        index = int(index)
        entry = dict(self.data.loc[index])
        print(index)
        curr_page = self.data.loc[index].image_path.replace('.jpg', '').replace('page_', '').replace('extra_', '').split('_')[0]
        pages_folder = '../page_images/PPM3/images'
        if isinstance(entry['image_path'], str):
            with open(os.path.join(self.image_folder, entry['image_path']), "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            entry['image_data'] = 'data:image/jpg;base64,' + encoded_string.decode('utf-8')
        else:
            entry['image_data'] = ''
            entry['image_path'] = ''

        if not isinstance(entry['raw_text'], str):
            entry['raw_text'] = ''
            entry['text'] = ''
            entry['id'] = ''

        with open(os.path.join(pages_folder, 'page_'+curr_page+'.jpg'), "rb") as image_file:
            encoded_page_string = base64.b64encode(image_file.read())
        entry['page_image'] = 'data:image/jpg;base64,' + encoded_page_string.decode('utf-8')

        del entry['text']

        return entry

    def shift_col_at_by(self, loc, n, col='image_path'):
        loc = int(loc)
        n = int(n)
        if 'image_path' in col:
            curr_page = self.data.loc[loc].image_path.replace('.jpg', '').replace('page_', '').replace('extra_', '').split('_')[0]
            for i in range(n):
                #self.data = self.data.append(pd.Series(), ignore_index=True)
                self.insert_extra_image_at_page(curr_page+'_'+str(i))

            self.load()
        #self.data.loc[loc:, col] = self.data.loc[loc:, col].shift(n)
        #self.data.loc[:loc+n, 'aligned'] = "yes"

    def insert_extra_image_at_page(self, page_no):
        def touch(path):
            with open(path, 'a'):
                os.utime(path, None)
        
        touch(os.path.join(self.image_folder, 'extra_page_{}.jpg'.format(page_no)))

    def save_progress(self, aligned_until):
        #self.data.loc[:aligned_until, 'aligned'] = "yes"
        #self.data.to_csv(self.data_csv+'.'+datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        with open('progress.txt', 'w') as f:
            f.write(aligned_until)

    def get_last_aligned_index(self):
        try:
            with open('progress.txt') as f:
                z = f.read()
        except:
            z = -1
        return int(z)
        #return self.data[self.data['aligned'] == 'no'].index[0] - 1 #Get to the first no.

    def load(self):
        chunk_align.get_current_alignment(self.image_folder, self.ocr_text, self.data_csv)
        self.data = pd.read_csv(self.data_csv)
        self.data.drop(['Unnamed: 0'], axis=1, inplace=True)

class RawDataLoader(object):
    def __init__(self, image_folder, raw_image_folder, marked_page_folder, load_previous_state=True):
        self.image_folder = image_folder
        self.raw_image_folder = raw_image_folder
        self.marked_page_folder = marked_page_folder
        self.load(load_previous_state)

    def load(self, load_previous_state):
        #sorted_pages = sorted([x.replace('.jpg', '').replace('page_', '') for x in os.listdir(self.raw_image_folder)], key=int)
        sorted_pages = sorted([(x.replace('.jpg', '').replace('page_', ''), x) for x in os.listdir(self.raw_image_folder)], key=lambda x:int(x[0]))
        sorted_pages = [x[1] for x in sorted_pages]
        self.mapping = []
        for page in sorted_pages:
            matches = glob.glob(os.path.join(self.image_folder, 'page_'+page.replace('.jpg', '').split('_')[-1]+'_*'))
            matches = [os.path.basename(x) for x in matches]
            sorted_matches = sorted([(x.replace('.jpg', '').replace('page_', ''), x) for x in matches], key=lambda x:int(x[0]))
            sorted_matches = [x[1] for x in sorted_matches]
            #print(os.path.join(self.image_folder, 'page_'+page.replace('.jpg', '').split('_')[-1]+'_*'))
            for match in sorted_matches:
                self.mapping.append((page, match))
            if len(matches) == 0:
                self.mapping.append((page, ''))

        #print(self.mapping[:5])

        #self.mapping = [(page, glob.glob(os.path.join(image_folder, page.replace('.jpg').split('_')[0]+'*'))) for page in sorted_pages]
        #self.count_mapping = [(tup[0], len(tup[1])) for tup in self.mapping]

        if not load_previous_state:
            with open('count_progress.txt', 'w') as f:
                f.write('0')

    def mark_page(self, page):
        shutil.copy(os.path.join(self.raw_image_folder, page), self.marked_page_folder)

    def unmark_page(self, page):
        os.remove(os.path.join(self.marked_page_folder, page))

    def get_data(self, index):
        index = int(index)
        entry = self.mapping[index]
        print(index)

        data_entry = {}

        with open(os.path.join(self.raw_image_folder, entry[0]), "rb") as image_file:
            encoded_page_string = base64.b64encode(image_file.read())
        data_entry['page_image'] = 'data:image/jpg;base64,' + encoded_page_string.decode('utf-8')
        data_entry['page_path'] = entry[0]

        if entry[1]:
            with open(os.path.join(self.image_folder, entry[1]), "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            data_entry['image_data'] = 'data:image/jpg;base64,' + encoded_string.decode('utf-8')
            data_entry['image_path'] = entry[1]
        else:
            data_entry['image_data'] = ''
            data_entry['image_path'] = ''

        return data_entry

    def save_progress(self, aligned_until):
        #self.data.loc[:aligned_until, 'aligned'] = "yes"
        #self.data.to_csv(self.data_csv+'.'+datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        with open('count_progress.txt', 'w') as f:
            f.write(aligned_until)

    def get_last_aligned_index(self):
        try:
            with open('count_progress.txt') as f:
                z = f.read()
        except:
            z = -1
        return int(z)
