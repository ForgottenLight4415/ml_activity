import os
import re

from flask import Blueprint, render_template, request, redirect, flash
from flask import current_app
from werkzeug.utils import secure_filename

from app.machine_learning.supervised import linear_regression

main = Blueprint('main', __name__)

model = None
info = None
results = None

def save_file(file_request):
    if 'training_file' not in file_request.files:
        flash("No file was uploaded for training")
        return redirect(file_request.url)
    else:
        file = file_request.files['training_file']
        if file.filename == '':
            flash('No selected file')
            return redirect(file_request.url);
        if file:
            with current_app.app_context() as app_context:
                file_path = os.path.join(
                        os.path.abspath(os.path.dirname(__file__)), 
                        app_context.app.config['UPLOAD_FOLDER'], 
                        secure_filename(file.filename)
                    )
                file.save(file_path) 
            flash('File uploaded successfully')
        return file_path

def supervised_algorithm(algorithm: str, data):
    if algorithm == 'linear_regression':
        return linear_regression(data)
        

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global model, info
        match request.form['form-type']:
            case 'training':
                file_path = save_file(request)
                if request.form['learning_method'] == 'supervised':
                    algorithm = request.form['algorithm']
                    model, info = supervised_algorithm(algorithm, file_path)
                    render_params = {
                        "model" : model,
                        "info" : info,
                        "result" : None,
                        "experiment_vals" : None
                    }
                    return render_template('index.html', render_args=render_params);
                elif request.form['learning_method'] == 'unsupervised':
                    pass
            case 'experiment':
                form_items = [[float(item[1]) for item in list(request.form.items())[1:]]]
                prediction = model.predict(form_items)
                render_params = {
                    "model" : model,
                    "info" : info,
                    "result" : prediction,
                    "experiment_vals" : form_items
                }
                return render_template('index.html', render_args=render_params);
        
    return render_template('index.html', render_args=None);
