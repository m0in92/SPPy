const parameterName = document.querySelector("select"); // user parameter name selection

parameterName.onclick = () => {
    let parameterSetName = document.querySelector("select").value;
    console.log(parameterSetName);
    document.getElementById("table_parameter_values_main_heading").innerHTML = parameterSetName;
    console.log('yes');
    fetch('static/parameter_sets.json')
        .then(response => response.json())
        .then(data => displayParametersetInformation(data[parameterSetName]));}

function displayParametersetInformation(data) {
    console.log(data);
    document.getElementById("id_parameter_values_vol_bc").innerHTML = data['Density_bc [kg m^-3]'];
}

