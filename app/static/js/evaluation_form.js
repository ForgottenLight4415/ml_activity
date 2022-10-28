async function submitEvaluationForm(e, evaluation_form) {
    e.preventDefault();
    const formData = new FormData(evaluation_form);
    const response = await fetch('http://127.0.0.1:5000/evaluate', {
        method: 'POST',
        body: formData
    });
    const result = await response.json();

    let expResultHTML = "<div class=\"experiment-vals\">\n" +
        "<table class=\"table\">\n" +
        "<thead>\n" +
        "<tr>\n" +
        "<th scope=\"col\">Parameter</th>\n" +
        "<th scope=\"col\">Information</th>\n" +
        "</tr>\n" +
        "</thead>\n" +
        "<tbody>\n";

    result["experiment_vals"].forEach(function (val) {
        expResultHTML += "<tr>\n" +
            "<th scope=\"row\">" + val[0] + "</th>\n" +
            "<td>" + val[1] + "</td>\n" +
            "</tr>\n";
    });

    expResultHTML += "</tbody>\n" +
    "</table>\n" +
    "</div>\n" +
    "<div class=\"results\">\n<h4>" + "Result: " + result["prediction"][0].toFixed(4) + "</h4>\n" +
    "</div>";

    const resultsSection = document.getElementById("results-section")
    resultsSection.innerHTML = expResultHTML
}

$(document).ready(function () {
    const evaluationForm = document.getElementById('evaluation-form');
    if (evaluationForm != null) {
        evaluationForm.addEventListener('submit', async function (e) {
            await submitEvaluationForm(e, evaluationForm);
        });
    }
});