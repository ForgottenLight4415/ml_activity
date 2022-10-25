var filePath = "";

function targetSelector(field, columns) {
    let optionHTML = '';
    for (let col of columns) {
        optionHTML += '<option value ="'  + col + '">' + col + '</option>';
    }
    field.innerHTML = optionHTML;
}

async function sumbitTrainingFormA(e, training_form) {
    e.preventDefault();
    const formData = new FormData(training_form);
    const response = await fetch('http://127.0.0.1:5000/submit/training/1', {
        method: 'POST',
        body: formData
    });

    const supervised_target_selection = document.getElementById("supervised_target_selection");
    if (formData.get("learning_method") === "supervised") {
        supervised_target_selection.style.display = "block";
    } else {
        supervised_target_selection.style.display = "none";
    }

    const result = await response.json();
    const targetField = document.getElementById("target_col_field");
    targetSelector(targetField, result["columns"]);
    filePath = result["file_path"];
    console.log(filePath);
}

async function sumbitTrainingFormB(e, trainingFormA, trainingFormB) {
    e.preventDefault();
    const formDataA = new FormData(trainingFormA);
    const formDataB = new FormData(trainingFormB);
    formDataA.delete("training_file");
    for (var [key, value] of formDataA) {
        formDataB.append(key, value);
    }
    formDataB.append("file_path", filePath);
    await fetch('http://127.0.0.1:5000/submit/training/2', {
        method: 'POST',
        body: formDataB
    }).then(function (response) {
        return response.text();
    }).then(function (html) {
        console.log(document.innerHTML)
        document.querySelector('html').innerHTML = html;
    });
}

function algoSelectionOptions(algoSelector, learning_method) {
    let optionHTML = '';
    if (learning_method == 'supervised') {
        let data = [
            ["linear_regression", "Linear Regression"], 
            ["logistic_regression", "Logistic Regression"], 
            ["svm", "Support Vector Machine (SVM)"], 
            ["random_forest", "Random Forest"]
        ]
        for(let opt of data) {
            optionHTML += '<option value ="'  + opt[0] + '">' + opt[1] + '</option>';
        }
        algoSelector.innerHTML = optionHTML;
    } else if (learning_method == 'unsupervised') {
        let data = [["knn", "K-Nearest Neighbours"], ["k-means", "K-Means"]];
        for(let opt of data) {
            optionHTML += '<option value ="'  + opt[0] + '">' + opt[1] + '</option>';
        }
        algoSelector.innerHTML = optionHTML;
    }
}

$(document).ready(function () {
    const learningMethod = document.getElementById('learning_method');
    const algorithm = document.getElementById('algorithm');

    algoSelectionOptions(algorithm, learningMethod.value);
    learningMethod.addEventListener('change', (event) => {
        algoSelectionOptions(algorithm, learningMethod.value);
    });

    const training_form = document.getElementById("training_form_a");
    training_form.addEventListener('submit', async function (e) {
        sumbitTrainingFormA(e, training_form);
    });

    const training_form_b = document.getElementById("training_form_b");
    training_form_b.addEventListener('submit', async function (e) {
        sumbitTrainingFormB(e, training_form, training_form_b);
    });
});