const parameterName = document.querySelector("select"); // user parameter name selection
fetchParametersetJson(parameterName.value); // displays the default parameter set value when the page loads

parameterName.onclick = () => {
    let parameterSetName = document.querySelector("select").value;
    document.getElementById("table_parameter_values_main_heading").innerHTML = parameterSetName;
    fetch('static/parameter_sets.json')
        .then(response => response.json())
        .then(data => displayParametersetInformation(data[parameterSetName]));}

function fetchParametersetJson(parameterSetName) {
    fetch('static/parameter_sets_ecm.json')
        .then(response => response.json())
        .then(data => displayParametersetInformation(data[parameterSetName]));
}

function displayParametersetInformation(data) {
    console.log(data)
}