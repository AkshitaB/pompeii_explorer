import os
import json
from flask import Flask, render_template, request, jsonify, url_for, redirect
import data

app = Flask(__name__)
app.config['data_loader'] = data.DataLoader('../final_extraction/PPM3-aligned.csv', '../final_extraction/PPM3', '../PPM/PPM_text_files/truncated/PPM-3ocr.txt')
app.config['raw_data_loader'] = data.RawDataLoader('../final_extraction/PPM3', '../page_images/PPM3/images', '../final_extraction/trial')

'''
To do:
save current idx.
'''

@app.route('/')
def index():
    return render_template('count_check.html', start_idx=app.config['raw_data_loader'].get_last_aligned_index())

@app.route('/align')
def align():
    return render_template('align.html', start_idx=app.config['data_loader'].get_last_aligned_index())

#using GET request so that index is visible to users and can be used to restart.
@app.route('/get_data_by_index', methods = ['GET'])
def get_data_by_index():
    data = request.args
    curr_idx = data['curr_idx']
    entry = app.config['data_loader'].get_data(curr_idx)
    strin = jsonify(entry)
    return strin

@app.route('/shift_alignment', methods = ['GET'])
def shift_alignment():
    data = request.args
    col_to_shift = data['col_to_shift']
    shift_at = data['shift_at']
    shift_by = data['shift_by']

    if col_to_shift == 'text':
        col_to_shift = ['id', 'raw_text', 'text']
    else:
        col_to_shift = ['image_path']

    app.config['data_loader'].shift_col_at_by(shift_at, shift_by, col=col_to_shift)

    print(app.config['data_loader'].data.loc[int(shift_at)])

    #save
    return "done"

@app.route('/save_progress', methods = ['GET'])
def save_progress():
    data = request.args
    curr_idx = data['curr_idx']
    app.config['data_loader'].save_progress(curr_idx)
    return "done"

@app.route('/reload', methods = ['GET'])
def reload():
    data = request.args
    app.config['data_loader'].load()
    return jsonify({'index_to_load': app.config['data_loader'].get_last_aligned_index()})
    #return "done"

@app.route('/mark_page', methods = ['GET'])
def mark_page():
    data = request.args
    page = data['page']
    app.config['raw_data_loader'].mark_page(page)
    return "done"

@app.route('/get_raw_data_by_index', methods = ['GET'])
def get_raw_data_by_index():
    data = request.args
    curr_idx = data['curr_idx']
    entry = app.config['raw_data_loader'].get_data(curr_idx)

    #print(entry['image_path'], entry['raw_text'], entry['id'])
    strin = jsonify(entry)
    return strin

@app.route('/save_raw_progress', methods = ['GET'])
def save_raw_progress():
    data = request.args
    curr_idx = data['curr_idx']
    app.config['raw_data_loader'].save_progress(curr_idx)
    return "done"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
