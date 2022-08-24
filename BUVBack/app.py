from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

import pandas as pd
import numpy as np
from sklearn.manifold import TSNE

import time

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
    A_data_path = '{}/data/{}/projection.csv'.format(FILE_ABS_PATH, 'NBA')
    B_data_path = '{}/data/{}/subspace.csv'.format(FILE_ABS_PATH, 'NBA')
    C_data_path = '{}/data/{}/breakdown.csv'.format(FILE_ABS_PATH, 'NBA')
    D_data_path = '{}/data/{}/bs.csv'.format(FILE_ABS_PATH, 'NBA')

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

def read_data(app_id):
    insight_path = '{}/data/{}/insight.csv'.format(FILE_ABS_PATH, app_id)
    subspace_path = '{}/data/{}/subspace.csv'.format(FILE_ABS_PATH, app_id)
    insight_df = pd.read_csv(insight_path)
    subspace_df = pd.read_csv(subspace_path)

    # only hard code for NBA
    insight_columns = insight_df.columns[:10]
    result_df = insight_df[insight_columns].merge(subspace_df, left_on='sid', right_on='sid')
    result_df['index'] = result_df.index
    insight_count = result_df[['insight', 'index']].groupby('insight').count().reset_index().to_dict('records')
    print('insight', insight_count)
    subspace_columns = list(subspace_df.columns)[:-1]
    print('subspace columns', subspace_columns)
    measure_values = result_df['measure'].unique().tolist()
    breakdown_count = result_df[['breakdown', 'index']].groupby('breakdown').count().reset_index().to_dict('records')
    subspace_statistics = {}
    for e in subspace_columns:
        subspace_statistics[e] = list(result_df[e].unique())
    return result_df, subspace_columns, measure_values, insight_count, breakdown_count, subspace_statistics

@app.route('/api/test/fetchDataByApp/', methods=['POST'])
def read_all_insight():
    params = request.json
    app_id = params['appID']
    result_df, subspace_columns, measure_values, insight_types, breakdown_count, subspace_statistics = read_data(app_id)

    projection_path = '{}/data/{}/projection.npz'.format(FILE_ABS_PATH, app_id)
    all_projection = np.load(projection_path)['projection']
    return json.dumps({
        'data': result_df.to_dict('records'),
        'subspace_columns': subspace_columns,
        'measure_values': measure_values,
        'projection': all_projection.tolist(),
        'insight_types': insight_types,
        'breakdown_count': breakdown_count,
        'subspace_statistics': subspace_statistics
    })

def generate_projection(sim_matrix, perplexity = 12):
    st = time.time()
    if sim_matrix.shape[0] == 0:
        return np.array([])
    if sim_matrix.shape[0] == 1:
        return np.array([[0,0]])
    X_embedded = TSNE(n_components=2,
                   init='random', perplexity=perplexity).fit_transform(sim_matrix)
    print('Projection use time', time.time() - st)
    return X_embedded

def calc_projection(sim, index_list, app_id, perplexity = 50):
    simFile = '{}/data/{}/similarity.npz'.format(FILE_ABS_PATH, app_id)
    matrix = np.load(simFile) if (type(sim) == str or sim is None) else sim
    matrix = matrix['sim']
    sub_matrix = matrix[index_list][:, index_list]
    X_embedded = generate_projection(sub_matrix, perplexity)
    return X_embedded

@app.route('/api/test/generateProjectionByApp/', methods=['POST'])
def return_projection():
    params = request.json
    app_id = params['appID']
    index_list = params['indexList']
    embedded = calc_projection(None, index_list, app_id, 50)
    return json.dumps(embedded.tolist())


if __name__ == '__main__':
    app.run()
