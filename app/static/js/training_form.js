$(document).ready(function () {
    let learningMethod = document.getElementById('learning_method');
    let algorithm = document.getElementById('algorithm');

    algoSelectionOptions(algorithm, learningMethod.value);
    learningMethod.addEventListener('change', (event) => {
        algoSelectionOptions(algorithm, learningMethod.value);
    });
});

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