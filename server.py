import os
import json
from flask import Flask, render_template, request, jsonify, url_for, redirect
import data

app = Flask(__name__)
app.config['data_loader'] = data.DataLoader('../final_extraction/PPM2-aligned.csv', '../final_extraction/PPM2')

'''
To do:
save current idx.
'''

@app.route('/')
def index():
   return render_template('align.html')

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
        col_to_shift = ['raw_text', 'text']
    else:
        col_to_shift = ['image_path']

    app.config['data_loader'].shiftColAtBy(shift_at, shift_by, col=col_to_shift)

    print(app.config['data_loader'].data)

    #save
    return "done"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
