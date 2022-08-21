from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

import pandas as pd

FILE_ABS_PATH = os.path.dirname(__file__)

app = Flask(__name__)
CORS(app)


@app.route('/api/test/counter/', methods=['POST'])
def update_counter():
    params = request.json
    counter = int(params['counter'])

    counter += 1

    resp = {'counter': counter}
    return jsonify(resp), 200, {"Content-Type": "application/json"}


@app.route('/api/test/hello/', methods=['POST'])
def hello_resp():
    params = request.json
    msg = int(params['msg'])
    print(msg)
    return "hello VUE"


@app.route('/api/test/fetchData/', methods=['POST'])
def fetch_data():
    A_data_path = '{}/data/projection.csv'.format(FILE_ABS_PATH)
    B_data_path = '{}/data/subspace.csv'.format(FILE_ABS_PATH)
    C_data_path = '{}/data/breakdown.csv'.format(FILE_ABS_PATH)
    D_data_path = '{}/data/bs.csv'.format(FILE_ABS_PATH)

    # with open(data_path, 'r') as input_file:
    #     data = json.load(input_file)
    #     return data

    A_df = pd.read_csv(A_data_path)
    A_results = A_df.to_dict('records')
    B_df = pd.read_csv(B_data_path)
    B_results = B_df.to_dict('records')
    C_df = pd.read_csv(C_data_path)
    C_results = C_df.to_dict('records')
    D_df = pd.read_csv(D_data_path)
    D_results = D_df.to_dict('records')

    return json.dumps({'A_results': A_results,
                       'B_results': B_results,
                       'C_results': C_results,
                       'D_results': D_results})

if __name__ == '__main__':
    app.run()
