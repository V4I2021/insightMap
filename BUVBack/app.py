from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

import pandas as pd
import numpy as np

from sklearn.manifold import TSNE
from sklearn.manifold import spectral_embedding
from dataService.dataService import DataService

import time


from sklearn.metrics import silhouette_score
from sklearn.cluster import AgglomerativeClustering

FILE_ABS_PATH = os.path.dirname(__file__)

app = Flask(__name__)
CORS(app)

dm = DataService()
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

def calc_value_count(name, subspace_columns):
    record_df = pd.read_csv('./data/{}/record.csv'.format(name))
    record_df = record_df[subspace_columns[:-1]]
    subspace_c = record_df.columns
    record_df['count'] = 1
    lists = []
    for column in subspace_c:
        dtype = record_df[column]
        r_df = record_df[[column, 'count']].groupby(column).count().reset_index()
        if record_df[column].dtypes == 'object':
            countList = r_df.sort_values('count', ascending=False).values.tolist()
            lists.append({'column': column, 'type': 'obj',  'list': countList})
        else:
            countList = r_df.sort_values(column, ascending=True).values.tolist()
            lists.append({'column':column, 'type': 'number', 'list': countList })
    return lists

def read_data(app_id):
    insight_path = '{}/data/{}/insight.csv'.format(FILE_ABS_PATH, app_id)
    subspace_path = '{}/data/{}/subspace.csv'.format(FILE_ABS_PATH, app_id)
    record_path = '{}/data/{}/record.csv'.format(FILE_ABS_PATH, app_id)

    insight_df = pd.read_csv(insight_path)
    subspace_df = pd.read_csv(subspace_path)
    record_df = pd.read_csv(record_path)

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

    record_df['count'] = 1
    lists = []
    for column in [c for c in record_df.columns if c not in ['count', 'cid']]:
        r_df = record_df[[column, 'count']].groupby(column).count().reset_index()
        if record_df[column].dtypes == 'object':
            countList = r_df.sort_values('count', ascending=False).values.tolist()
            lists.append({'column': column, 'type': 'obj',  'list': countList})
        else:
            countList = r_df.sort_values(column, ascending=True).values.tolist()
            lists.append({'column': column, 'type': 'number', 'list': countList })

    return result_df, subspace_columns, measure_values, insight_count, breakdown_count, subspace_statistics, lists

@app.route('/api/test/fetchDataByApp/', methods=['POST'])
def read_all_insight():
    params = request.json
    app_id = params['appID']
    result_df, subspace_columns, measure_values, insight_types, breakdown_count, subspace_statistics, subspace_raw_count = read_data(app_id)

    projection_path = '{}/data/{}/projection.npz'.format(FILE_ABS_PATH, app_id)
    all_projection = np.load(projection_path)['projection']
    simFile = '{}/data/{}/similarity.npz'.format(FILE_ABS_PATH, app_id)
    matrix = np.load(simFile)['sim']
    return json.dumps({
        'data': result_df.to_dict('records'),
        'subspace_columns': subspace_columns,
        'measure_values': measure_values,
        'projection': all_projection.tolist(),
        'insight_types': insight_types,
        'breakdown_count': breakdown_count,
        'subspace_statistics': subspace_statistics,
        'sim_matrix': matrix.tolist(),
        'subspace_raw_count': subspace_raw_count
    })

def generate_projection(sim_matrix, perplexity):
    st = time.time()
    if sim_matrix.shape[0] == 0:
        return np.array([])
    if sim_matrix.shape[0] == 1:
        return np.array([[0,0]])
    # Plan 1
    X_embedded = TSNE(n_components=2,
                   init='random', perplexity=perplexity).fit_transform(sim_matrix)

    # Plan 2
    # X_embedded = spectral_embedding(sim_matrix,
    #                                 eigen_solver="lobpcg",
    #                                 norm_laplacian=True,
    #                                 n_components=2)

    # Plan 3
    # grah_embedding = spectral_embedding(sim_matrix, n_components=12)

    # X_embedded = TSNE(n_components=2,
    #                init='random', perplexity=perplexity).fit_transform(grah_embedding)

    print('Projection use time', time.time() - st)
    return X_embedded

def calc_projection(sim, index_list, app_id, perplexity):
    simFile = '{}/data/{}/similarity.npz'.format(FILE_ABS_PATH, app_id)
    matrix = np.load(simFile) if (type(sim) == str or sim is None) else sim
    matrix = matrix['sim']
    sub_matrix = matrix[index_list][:, index_list]
    X_embedded = generate_projection(sub_matrix, perplexity)
    return X_embedded


def best_clustering(X_embedded, min_cluster=2, max_cluster=50):
    max_score = -1
    max_labels = None
    max_n = -1
    for i in range(min_cluster, max_cluster):
        clustering = AgglomerativeClustering(n_clusters=i).fit(X_embedded)
        score = silhouette_score(
            X_embedded,
            clustering.labels_,
            metric="euclidean",
        )

        if max_score < score:
            max_score = score
            max_labels = clustering.labels_
            max_n = i
    print('Max cluster number {}, best cluster number {}'.format(max_cluster, max_n))
    return max_score, max_n, max_labels

def calc_projection_with_cluster(sim, index_list, app_id, perplexity):
    simFile = '{}/data/{}/similarity.npz'.format(FILE_ABS_PATH, app_id)
    matrix = np.load(simFile) if (type(sim) == str or sim is None) else sim
    matrix = matrix['sim']
    sub_matrix = matrix[index_list][:, index_list]
    X_embedded = generate_projection(sub_matrix, perplexity)
    score, n, labels = best_clustering(X_embedded, max_cluster=min(50, X_embedded.shape[0]))
    return X_embedded, labels

@app.route('/api/test/generateProjectionByApp/', methods=['POST'])
def return_projection():
    params = request.json
    app_id = params['appID']
    index_list = params['indexList']
    start_time = time.time()
    embedded, labels = calc_projection_with_cluster(None, index_list, app_id, 25)
    merge_list = np.concatenate((embedded, labels.reshape(labels.shape[0], 1)), axis=1)
    print('Use time', time.time() - start_time)
    return json.dumps(merge_list.tolist())

@app.route('/api/test/getInsightByIID/', methods=['POST'])
def getInsightByIID():
    st = time.time()
    params = request.json
    app_id = params['appID']
    iid = params['iid']

    result = dm.get_insight_by_iid(iid, app_id)
    print('Query insight use time: ', app_id, iid, time.time() - st)
    result['iid'] = iid
    return result

if __name__ == '__main__':
    app.run()
    # st = time.time()
    #
    # dm = DataService()
    # result = dm.get_insight_by_iid(110, 'NBA')
    # print('rrrr', result)
    # print('time.time', time.time() - st)