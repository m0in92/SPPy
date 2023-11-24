const parameterName = document.querySelector("select");
parameterName.onclick = () => {document.getElementById("th_parameter_name").innerHTML = document.querySelector("select").value};