function targetSelector(field, columns) {
    let optionHTML = '';
    for (let col of columns) {
        optionHTML += '<option value ="'  + col + '">' + col + '</option>';
    }
    field.innerHTML = optionHTML;
}

function dropColumnCheckBoxGenerator(div, columns) {
    let checkBoxHTML = '';
    for (let col of columns) {
        checkBoxHTML += "<div class=\"form-check\">\n" +
            "  <input class=\"form-check-input\" type=\"checkbox\" name='check_" + col + "' value=\"" + col + "\"" +
            "  <label class=\"form-check-label\" for=\"check_" + col + "\">\n" +
            "    " + col + "\n" +
            "  </label>\n" +
            "</div>";
    }
    div.innerHTML = checkBoxHTML;
}

async function sumbitTrainingFormA(e, training_form) {
    e.preventDefault();
    const formData = new FormData(training_form);
    const response = await fetch('http://127.0.0.1:5000/submit/training/1', {
        method: 'POST',
        body: formData
    });

    const supervised_target_selection = document.getElementById("target_selection");
    supervised_target_selection.style.display = "block";

    const result = await response.json();
    const targetField = document.getElementById("target_col_field");
    targetSelector(targetField, result["columns"]);

    const dropColCheckBoxes = document.getElementById("drop-checkboxes");
    dropColumnCheckBoxGenerator(dropColCheckBoxes, result["columns"]);

    const additionalAttributes = document.getElementById("additional-options");
    if (result['additional_data'] != null) {
        additionalAttributes.style.display = "block";
        let formHTML = '';

        result['additional_data'].forEach(function (val) {
           formHTML += "<label for=\"" + val[1] + "\" class=\"form-label\">Select" + val[2] + "</label>\n";
           if (val[0] === 'select') {
               formHTML += "<select class=\"form-select\" id=\"" + val[1] + "\" name=\"" + val[1] + "\"></select>"
           } else if (val[0] === 'text') {
               formHTML += "<input type=\"text\" class=\"form-control\" name=\"" + val[1] + "\">"
           }
        });

        additionalAttributes.innerHTML = formHTML;

    } else {
        additionalAttributes.style.display = "none";
    }
}

function algoSelectionOptions(algoSelector, learning_method) {
    let optionHTML = '';
    if (learning_method === 'supervised') {
        let data = [
            ["linear_regression", "Linear Regression"],
        ]
        for(let opt of data) {
            optionHTML += '<option value ="'  + opt[0] + '">' + opt[1] + '</option>';
        }
        algoSelector.innerHTML = optionHTML;
    } else if (learning_method === 'unsupervised') {
        let data = [
            ["hierarchical_clustering", "Hierarchical Clustering"],
            ["pca", "Principal Component Analysis (PCA)"],
            // ["knn", "K-Nearest Neighbours"],
            // ["k-means", "K-Means"]
        ];
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
    learningMethod.addEventListener('change', (_) => {
        algoSelectionOptions(algorithm, learningMethod.value);
    });

    const training_form = document.getElementById("training_form_a");
    training_form.addEventListener('submit', async function (e) {
        await sumbitTrainingFormA(e, training_form);
    });
});