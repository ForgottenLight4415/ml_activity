import json
import pandas as pd

from flask import Blueprint, request, render_template

from app.utilities import save_file, supervised_algorithm

main = Blueprint('main', __name__)

model = None
info = None

@main.route('/')
def index():
    return render_template('index.html', render_args=None)

@main.route('/submit/training/<step>', methods=['POST'])
def handleTrainingRequests(step):
    step = int(step)
    if step == 1:
        file_path = save_file(request)
        df = pd.read_csv(file_path)
        df_cols = ["{}".format(col) for col in df.columns]
        return json.dumps({
            "columns" : df_cols,
            "file_path" : file_path
        })
    elif step == 2:
        algorithm = request.form['algorithm']
        file_path = request.form['file_path']
        target = request.form['target']
        global model, info
        model, info = supervised_algorithm(algorithm, target, file_path)
        render_params = {
            "info" : info,
            "result" : None,
            "experiment_vals" : None
        }
        return render_template('results.html', render_args=render_params)
    else:
        return json.dumps("Exited")

@main.route('/evaluate', methods=['POST'])
def handleEvaluation():
    data = [[int(request.form[val]) for val in request.form]]
    global model
    pred = model.predict(data)
    render_params = {
        "info" : info,
        "result" : pred,
        "experiment_vals" : data
    }
    return render_template('results.html', render_args=render_params)