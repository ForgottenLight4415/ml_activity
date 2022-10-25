import os

from flask import redirect, flash
from flask import current_app
from werkzeug.utils import secure_filename

from .machine_learning.supervised import *

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

def supervised_algorithm(algorithm: str, target: str, data):
    if algorithm == 'linear_regression':
        return linear_regression(data, target)