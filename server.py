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
   return render_template('index.html')

#using GET request so that index is visible to users and can be used to restart.
@app.route('/get_data_by_index', methods = ['GET'])
def get_data_by_index():
    data = request.args
    print(data)
    curr_idx = data['curr_idx']
    print(curr_idx)
    entry = app.config['data_loader'].get_data(curr_idx)
    print(entry['id'])

    strin = jsonify(entry)
    print(strin)
    return strin

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
