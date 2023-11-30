const parameterName = document.querySelector("select"); // user parameter name selection
fetchParametersetJson(parameterName.value); // displays the default parameter set value when the page loads

parameterName.onclick = () => {
    let parameterSetName = document.querySelector("select").value;
    document.getElementById("table_parameter_values_main_heading").innerHTML = parameterSetName;
    fetch('static/parameter_sets.json')
        .then(response => response.json())
        .then(data => displayParametersetInformation(data[parameterSetName]));}

function fetchParametersetJson(parameterSetName) {
    fetch('static/parameter_sets.json')
        .then(response => response.json())
        .then(data => displayParametersetInformation(data[parameterSetName]));
}

function displayParametersetInformation(data) {
    // positive electrode parameters are updated below
    document.getElementById("id_parameter_value_diffusivity_p").innerHTML = data["Reference Diffusitivity_p [m^2 s^-1]"];
    document.getElementById("id_parameter_value_reaction_rate_p").innerHTML = data["Reference Rate Constant_p [m^2.5 mol^-0.5 s^-1]"];
    document.getElementById("id_parameter_value_particle_radius_p").innerHTML = data["Radius_p [m]"];
    document.getElementById("id_parameter_value_volume_fraction_p").innerHTML = data["Volume Fraction_p"];
    document.getElementById("id_parameter_value_anodic_transfer_coefficient_p").innerHTML = data["Anodic Transfer Coefficient_p"];
    document.getElementById("id_parameter_value_cathodic_transfer_coefficient_p").innerHTML = 1 - data["Anodic Transfer Coefficient_p"];
    document.getElementById("id_parameter_value_bruggerman_coefficient_p").innerHTML = data["Bruggerman Coefficient_p"];
    document.getElementById("id_parameter_value_max_conc_p").innerHTML = data["Max. Conc._p [mol m^-3]"];

    // seperator parameters are updated below
    document.getElementById("id_parameter_value_volume_fraction_sep").innerHTML = data["Volume Fraction_sep"];
    document.getElementById("id_parameter_value_bruggerman_coefficient_sep").innerHTML = data["Bruggerman Coefficient_sep"];

    // negative electrode parameters are updated below
    document.getElementById("id_parameter_value_diffusivity_n").innerHTML = data["Reference Diffusitivity_n [m^2 s^-1]"];
    document.getElementById("id_parameter_value_reaction_rate_n").innerHTML = data["Reference Rate Constant_n [m^2.5 mol^-0.5 s^-1]"];
    document.getElementById("id_parameter_value_particle_radius_n").innerHTML = data["Radius_n [m]"];
    document.getElementById("id_parameter_value_volume_fraction_n").innerHTML = data["Volume Fraction_n"];
    document.getElementById("id_parameter_value_anodic_transfer_coefficient_n").innerHTML = data["Anodic Transfer Coefficient_n"];
    document.getElementById("id_parameter_value_cathodic_transfer_coefficient_n").innerHTML = 1 - data["Anodic Transfer Coefficient_n"];
    document.getElementById("id_parameter_value_bruggerman_coefficient_n").innerHTML = data["Bruggerman Coefficient_n"];
    document.getElementById("id_parameter_value_max_conc_n").innerHTML = data["Max. Conc._n [mol m^-3]"];

    // the battery cell parameters are updated below
    document.getElementById("id_parameter_values_cross_section_area_bc").innerHTML = data["Electrode Area_n [m^2]"];
    document.getElementById("id_parameter_values_density_bc").innerHTML = data['Density_bc [kg m^-3]'];
    document.getElementById("id_parameter_values_volume_bc").innerHTML = data["Volume_bc [m^3]"];
    document.getElementById("id_parameter_values_specific_heat_bc").innerHTML = data["Specific Heat_bc [J K^-1 kg^-1]"];
    document.getElementById("id_parameter_heat_transfer_coefficient_bc").innerHTML = data["Heat Transfer Coefficient_bc [J s^-1 K^-1]"];
    document.getElementById("id_parameter_surface_area_bc").innerHTML = data["Surface Area_bc [m^2]"];
    document.getElementById("id_parameter_value_capacity_bc").innerHTML = data["Capacity_bc [A hr]"];
    document.getElementById("id_parameter_max_potential_value_bc").innerHTML = data["Maximum Potential Cut-off_bc [V]"];
    document.getElementById("id_parameter_min_potential_value_bc").innerHTML = data["Minimum Potential Cut-off_bc [V]"];
}

// displayParametersetInformation()

// function plotTimeVoltage(time, voltage) {
//     const ctx = document.getElementById('id_chart');
//
//     const config = {type: 'line',
//         data: {
//         labels: time,
//             datasets: [{
//             // label: '# of Votes',
//                 data: voltage,
//                 borderWidth: 1,
//                 backgroundColor: 'black'
//         }]},
//         options: {
//         scales: {
//             y: {
//                 beginAtZero: false
//             }
//         }
//     }
//     }
//
//     var chartObj = new Chart(ctx, config);
//     // chartObj.destroy();
// }
//
//
// async function createPlot() {
//     let response = await fetch('', {
//         method: 'get',
//         headers: {
//             'X-Requested-With': 'XMLHttpRequest',
//             'Content-Type': 'application/json'
//         },
//     });
//
//     let data = await response.json();
//     plotTimeVoltage(data['t [s]'], data['V [V]'])
//     console.log(await data);
// }



