import io
import json
import pandas as pd

from flask import Blueprint, Response, request, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from app.utilities import save_file, supervised_algorithm

main = Blueprint('main', __name__)

file_path = None
target = None
model = None
info = None

X_train = None
X_test = None
y_train = None
X_test = None
pred = None

@main.route('/')
def index():
    return render_template('index.html', render_args=None)

@main.route('/submit/training/<step>', methods=['POST'])
def handleTrainingRequests(step):
    step = int(step)
    if step == 1:
        global file_path
        file_path = save_file(request)
        df = pd.read_csv(file_path)
        df_cols = ["{}".format(col) for col in df.columns]
        return json.dumps({
            "columns" : df_cols,
            "file_path" : file_path
        })
    elif step == 2:
        algorithm = request.form['algorithm']
        # file_path = request.form['file_path']
        global target
        target = request.form['target']
        global model, info, X_train, X_test, y_train, y_test, pred
        model, info, X_train, X_test, y_train, y_test, pred = supervised_algorithm(algorithm, target, file_path)
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

@main.route('/image')
def plot_image():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.scatter(X_train, y_train)
    axis.plot(X_test, pred, c='orange')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
