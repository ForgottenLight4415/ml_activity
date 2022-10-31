import re
import json
import pandas as pd

from flask import Blueprint, request, render_template
from app.utilities import save_file
from app.machine_learning.data_model import DataModel

main = Blueprint('main', __name__)

dm: DataModel | None = None


@main.route('/')
def index():
    return render_template('index.html', render_args=None)


@main.route('/submit/training/<step>', methods=['POST'])
def handle_training_request(step):
    global dm
    step = int(step)
    if step == 1:
        file_path = save_file(request)
        df = pd.read_csv(file_path)
        learning_method = request.form["learning_method"]
        algorithm = request.form["algorithm"]
        dm = DataModel(df, learning_method, algorithm)

        return_data = {
            "columns": dm.column_names
        }

        if learning_method == "unsupervised":
            if algorithm == "hierarchical_clustering":
                return_data['additional_data'] = [('text', 'n_clusters', ' number of clusters')]
            elif algorithm == "pca":
                return_data['additional_data'] = [('text', 'n_components', ' number of components')]

        return json.dumps(return_data)
    elif step == 2:
        drop_cols = list()
        target = request.form['target']
        for k, v in request.form.items():
            if re.match("^check_.*", k):
                drop_cols.append(v)
        exp = True
        usuper = False
        if dm and target:
            if len(request.form) == 1:
                dm.train_model(target, drop_cols)
                if dm.algorithm_name == "kmeans":
                    dm.train_model(target, drop_cols)
                    usuper = True
            else:
                if dm.algorithm_name == "hierarchical_clustering":
                    dm.train_model(target, drop_cols, n_clusters=int(request.form['n_clusters']))
                    exp = False
                elif dm.algorithm_name == "pca":
                    dm.train_model(target, drop_cols, n_components=int(request.form['n_components']))
                    exp = False
            exp_cols = list(dm.column_names)
            exp_cols.remove(dm.target)
            render_params = {
                "info": dm.model_info,
                "exp_cols": exp_cols
            }
            if render_params["info"] is not None:
                return render_template(
                    'post_train/results.html', render_args=render_params, experiment=exp, usuper=usuper
                )
            else:
                return render_template('error.html', error_message="Something went wrong")
        else:
            return render_template('error.html', error_message="Model not available")
    else:
        return render_template('error.html', error_message="Invalid step")


@main.route('/evaluate', methods=['POST'])
def evaluate():
    if "clusters" in request.form.keys():
        print("Here")
        return json.dumps({
            "experiment_vals": [val for val in zip(['Clusters'], [request.form['clusters']])],
            "prediction": ["Graph plotted"],
            "graph": True
        })
    data = [[float(request.form[val]) for val in request.form]]
    print(data)
    global dm
    pred = dm.make_predictions(data)
    exp_cols = list(dm.column_names)
    exp_cols.remove(dm.target)
    return json.dumps({
        "experiment_vals": [val for val in zip(dm.column_names, data)],
        "prediction": list(pred)
    })


@main.route('/image')
def plot_image():
    global dm
    if dm:
        print("Generating plot")
        return dm.make_image()
    else:
        return "<h3>Could not generate a plot. Insufficient data</h3>"


@main.route('/evaluation/image')
def evaluate_image():
    global dm
    if dm:
        print("Generating plot")
        return dm.evaluate_image(int(request.args.get("clusters")))
    else:
        return "<h3>Could not generate a plot. Insufficient data</h3>"
