import os
import re
import pandas as pd

#chunk_start_pattern = re.compile('[0-9]+\.{1}')
chunk_start_pattern = re.compile('[0-9]+a?-?[b-z]{0,1}\.{1}\s')
chunk_multiple_pattern = re.compile('[0-9]+a?-?[0-9]+a?\.{1}\s')
#negative_pattern = re.compile("^([A-Z\s]{4,5}[0-9\s]{4,6})|^([0-9\s]{2,3}[A-Z\s]{4,5}[0-9\s]{4,6})")
negative_pattern = re.compile("^([A-Z\s]{4,5}[0-9\s]{4,6})|^([0-9\s]{2,3}[A-Z\s]{1,5}[0-9\s]{4,6})")
negative_pattern_find_all = re.compile("([A-Z\s]{4,5}[0-9\s]{4,6})|([0-9\s]{2,3}[A-Z\s]{4,5}[0-9\s]{4,6})")

def is_negative(line):
    line = line.replace(' ', '')
    if negative_pattern.match(line) \
    or 'Diap.' in line \
    or line.startswith('AFS') \
    or line.startswith('DAIR') \
    or 'GFN' in line \
    or 'deVos' in line \
    or 'GFXEK' in line \
    or 'Spinazzola,fig.' in line:
        return True
    return False

class Chunk(object):
    def __init__(self, raw):
        self.text = ''
        self.id = []
        self.raw_text = ''
        self.__process__(raw)
        
    def __process__(self, raw):
        #self.text = ''.join([line.replace('\n', '') for line in raw])
        #if negative_pattern.match(raw[-1]):
        last_line = ''
        for i, line in enumerate(raw):
            if i == 0:
                line = line.replace(line.split('.')[0]+'. ', '')
            #print(line)
            line = line.replace('\n', '')
            line = line.replace('\r', '')
            line = line.replace('\t', ' ')
            line = line.replace('\x92', '\'')
            if line != '' and line != '\x0c':
                #print('??')
                if is_negative(line):
                    self.id.append(line.replace(' ', ''))
                else:
                    self.text += line
                last_line = line
                
        #print(self.id)
                
        if not self.id:
            self.id = ['Unknown']
        
#         last_line = last_line.replace(' ','')
#         if negative_pattern.match(last_line) or 'Diag.' in last_line:
#             self.id.append(last_line)
#         else:
#             self.id.append('NA')
        self.raw_text = ''.join(raw)
    
    def __repr__(self):
        return str(self.__dict__)

def extract_chunks(ppm_text, chunk_start_pattern):
    curr_chunk = []
    all_chunks = []
    raw_chunks = []
    num_times = 1
    for line in ppm_text:
        line = line.decode('utf-8-sig', errors='ignore')
        if chunk_start_pattern.match(line):
            if curr_chunk:
                for tim in range(num_times):
                    all_chunks.append(Chunk(curr_chunk))
                    raw_chunks.append(curr_chunk)
                num_times = 1
            curr_chunk = []
            match = chunk_start_pattern.findall(line)[0]
            if 'a-' in match:
                #print(line)
                last_char = match.split('-')[1].split('.')[0]
                #print(last_char)
                num_times = ord(last_char) - 97 + 1
        elif chunk_multiple_pattern.match(line):
            #print(line)
            if curr_chunk:
                for tim in range(num_times):
                    all_chunks.append(Chunk(curr_chunk))
                    raw_chunks.append(curr_chunk)
                num_times = 1
            curr_chunk = []
            match = chunk_multiple_pattern.findall(line)[0]
            tmp = match.replace('.', '').split('-')
            fir = tmp[0]
            sec = tmp[1]
            num_times = int(sec) - int(fir) + 1

        curr_chunk.append(line)
    return all_chunks, raw_chunks

def get_current_alignment(data_folder, ocr_text, save_alignment):
    ppm_text = []
    with open(os.path.join(ocr_text), 'rb') as f:
        ppm_text = f.readlines()

    all_chunks, raw_chunks = extract_chunks(ppm_text, chunk_start_pattern)
    ppm_data = pd.DataFrame([chunk.__dict__ for chunk in all_chunks])
    ppm_data['id'] = ppm_data['id'].apply(lambda x:','.join(x))

    sorted_img_ids = sorted([(x.replace('.jpg', '').replace('page_', '').replace('extra_', ''), x) for x in os.listdir(data_folder) if 'unaligned' not in x and 'temp' not in x], key=lambda x:int(x[0]))
    sorted_img_ids = [x[1] for x in sorted_img_ids]

    for i in range(len(ppm_data)-len(sorted_img_ids)):
        sorted_img_ids.append(None)

    ppm_data['image_path'] = sorted_img_ids[:len(ppm_data)]

    ppm_data.to_csv(save_alignment)
